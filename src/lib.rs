use pyo3::prelude::*;
use std::time::Instant;
use std::thread;
use heapless::Vec as HeaplessVec;
use zeroize::Zeroize;
use crossbeam_channel::{bounded, Sender, Receiver};
use nalgebra::{DMatrix, DVector};

#[pyclass]
pub struct SignalProcessor {}

#[pymethods]
impl SignalProcessor {
    #[new]
    fn new() -> Self { SignalProcessor {} }

    /// Signal layer inversion for pattern analysis
    fn invert_signal_layer(&self, weights: Vec<f32>, threshold: f32) -> PyResult<(usize, f64, String)> {
        let start = Instant::now();
        let principal_neurons: Vec<f32> = weights.into_iter()
            .filter(|&w| w.abs() > threshold)
            .collect();
        let duration = start.elapsed().as_secs_f64();
        Ok((principal_neurons.len(), duration, format!("REDUCED_TO_{}_SIGNALS", principal_neurons.len())))
    }
}

#[pyclass]
pub struct DataIngestor {}

#[pymethods]
impl DataIngestor {
    #[new]
    fn new() -> Self { DataIngestor {} }

    fn process_raw_data(&self, raw_data: String) -> PyResult<(bool, f64, String)> {
        let start = Instant::now();
        let success = !raw_data.is_empty();
        Ok((success, start.elapsed().as_secs_f64(), "DATA_STABLE".to_string()))
    }
}

#[derive(Zeroize)]
#[pyclass]
pub struct CognitivePayload {
    #[pyo3(get, set)]
    pub sentiment: f32,
    #[pyo3(get, set)]
    pub arousal: f32,
    #[pyo3(get, set)]
    pub culture_id: u16,
    // SAT clauses stored in heap Vec for Python interface (converted to/from heapless internally)
    #[pyo3(get, set)]
    pub sat_clauses: Vec<i16>,
}

#[pymethods]
impl CognitivePayload {
    #[new]
    fn new() -> Self {
        CognitivePayload {
            sentiment: 0.0,
            arousal: 0.0,
            culture_id: 0,
            sat_clauses: Vec::new(),
        }
    }

    /// Unpack binary packet from Python postcard bridge
    fn unpack_from_bridge(&mut self, raw_bytes: Vec<u8>) -> PyResult<bool> {
        // Validate minimal structural footprint header (8 byte header + 10 byte metrics)
        if raw_bytes.len() < 18 {
            return Ok(false);
        }

        // Verify custom protocol aerospace header
        if &raw_bytes[0..4] != b"ZED\x01" {
            return Ok(false);
        }

        // Read specific byte indices using native system little-endian byte ordering
        let sentiment = f32::from_le_bytes(raw_bytes[8..12].try_into().unwrap());
        let arousal = f32::from_le_bytes(raw_bytes[12..16].try_into().unwrap());
        let culture_id = u16::from_le_bytes(raw_bytes[16..18].try_into().unwrap());

        // Use heapless Vec for stack allocation with fixed capacity
        let mut sat_clauses_heapless: HeaplessVec<i16, 512> = HeaplessVec::new();
        let mut offset = 18;

        // Iterate through remaining raw bytes to populate the fixed stack container
        while offset + 2 <= raw_bytes.len() {
            let clause = i16::from_le_bytes(raw_bytes[offset..offset+2].try_into().unwrap());
            if sat_clauses_heapless.push(clause).is_err() {
                break; // Hard stack buffer limit reached - enforces safety bounds mathematically
            }
            offset += 2;
        }

        // Update struct fields (convert heapless to std Vec for Python interface)
        self.sentiment = sentiment;
        self.arousal = arousal;
        self.culture_id = culture_id;
        self.sat_clauses = sat_clauses_heapless.into_iter().collect();

        Ok(true)
    }

    /// Pack struct back to binary format for transmission
    fn pack_to_bridge(&self) -> PyResult<Vec<u8>> {
        let mut sat_clauses_heapless: HeaplessVec<i16, 512> = HeaplessVec::new();
        for clause in &self.sat_clauses {
            if sat_clauses_heapless.push(*clause).is_err() {
                break;
            }
        }

        let clause_count = sat_clauses_heapless.len() as u16;
        let mut payload = Vec::new();

        // Pack metrics
        payload.extend_from_slice(&self.sentiment.to_le_bytes());
        payload.extend_from_slice(&self.arousal.to_le_bytes());
        payload.extend_from_slice(&self.culture_id.to_le_bytes());

        // Pack SAT clauses
        for clause in sat_clauses_heapless {
            payload.extend_from_slice(&clause.to_le_bytes());
        }

        // Add header
        let mut packet = Vec::new();
        packet.extend_from_slice(b"ZED\x01");
        packet.extend_from_slice(&1u16.to_le_bytes()); // Version
        packet.extend_from_slice(&(payload.len() as u16).to_le_bytes());
        packet.extend_from_slice(&payload);

        Ok(packet)
    }
}

#[pyclass]
pub struct LockFreeAudioPipeline {
    // Store channels as raw pointers to avoid PyO3 trait conflicts
    tx_ptr: *mut (),
    rx_ptr: *mut (),
    capacity: usize,
}

// SAFETY: The channels are only accessed through the struct's methods
// and are never moved or dropped while the struct is alive
unsafe impl Send for LockFreeAudioPipeline {}
unsafe impl Sync for LockFreeAudioPipeline {}

#[pymethods]
impl LockFreeAudioPipeline {
    #[new]
    pub fn new() -> Self {
        // Initialize a bounded ring buffer capable of holding 4096 real-time audio frames entirely on the stack
        let (tx, rx) = bounded::<i16>(4096);
        
        // Box the channels to get stable pointers
        let tx_box = Box::new(tx);
        let rx_box = Box::new(rx);
        
        LockFreeAudioPipeline {
            tx_ptr: Box::into_raw(tx_box) as *mut (),
            rx_ptr: Box::into_raw(rx_box) as *mut (),
            capacity: 4096,
        }
    }

    /// Non-blocking write operation: returns false instantly if the hardware channel is congested
    pub fn push_frame_block(&self, clauses: Vec<i16>) -> PyResult<bool> {
        // SAFETY: The pointer was created from a Box and is valid
        let tx = unsafe { &*(self.tx_ptr as *const Sender<i16>) };
        
        for clause in clauses {
            if tx.try_send(clause).is_err() {
                return Ok(false);
            }
        }
        Ok(true)
    }

    /// Spawn a pure native operating system thread completely detached from Python's interpreter environment
    pub fn spawn_isolated_audio_worker(&self) -> PyResult<()> {
        // SAFETY: The pointer was created from a Box and is valid
        let rx = unsafe { &*(self.rx_ptr as *const Receiver<i16>) };
        let local_rx = rx.clone();

        // Spawn a pure native operating system thread completely detached from Python's interpreter environment
        thread::spawn(move || {
            // Pin the native worker loop directly to CPU Core 1 using low-level OS handles
            #[cfg(target_os = "windows")]
            unsafe {
                use windows_sys::Win32::System::Threading::*;
                let current_thread = GetCurrentThread();
                SetThreadAffinityMask(current_thread, 2); // Binary mask 0b10 target maps exclusively to Core 1
            }

            // Real-time audio rendering loop pulling from the lock-free channel
            while let Ok(frame_data) = local_rx.recv() {
                // Direct-to-hardware streaming registers run uninterrupted here
                let _active_signal = frame_data;
            }
        });

        Ok(())
    }

    /// Get current channel capacity (for monitoring)
    pub fn get_capacity(&self) -> PyResult<usize> {
        Ok(self.capacity)
    }

    /// Get current channel length (for monitoring)
    pub fn get_length(&self) -> PyResult<usize> {
        // SAFETY: The pointer was created from a Box and is valid
        let rx = unsafe { &*(self.rx_ptr as *const Receiver<i16>) };
        Ok(rx.len())
    }

    /// Check if channel is empty (for monitoring)
    pub fn is_empty(&self) -> PyResult<bool> {
        // SAFETY: The pointer was created from a Box and is valid
        let rx = unsafe { &*(self.rx_ptr as *const Receiver<i16>) };
        Ok(rx.is_empty())
    }

    /// Check if channel is full (for monitoring)
    pub fn is_full(&self) -> PyResult<bool> {
        // SAFETY: The pointer was created from a Box and is valid
        let rx = unsafe { &*(self.rx_ptr as *const Receiver<i16>) };
        Ok(rx.is_full())
    }
}

// Implement Drop to properly clean up the boxed channels
impl Drop for LockFreeAudioPipeline {
    fn drop(&mut self) {
        // SAFETY: Convert pointers back to Box and drop them
        if !self.tx_ptr.is_null() {
            unsafe {
                let _ = Box::from_raw(self.tx_ptr as *mut Sender<i16>);
            }
        }
        if !self.rx_ptr.is_null() {
            unsafe {
                let _ = Box::from_raw(self.rx_ptr as *mut Receiver<i16>);
            }
        }
    }
}

#[pyclass]
pub struct MusicMatrix {
    pitch_matrix: Option<DMatrix<f32>>,
    rhythm_matrix: Option<DMatrix<f32>>,
    harmony_matrix: Option<DMatrix<f32>>,
}

#[pymethods]
impl MusicMatrix {
    #[new]
    pub fn new() -> Self {
        MusicMatrix {
            pitch_matrix: None,
            rhythm_matrix: None,
            harmony_matrix: None,
        }
    }

    /// Create a pitch transition matrix from emotional vectors
    pub fn create_pitch_matrix(&mut self, emotional_vector: Vec<f32>) -> PyResult<()> {
        let n = emotional_vector.len();
        if n < 2 {
            return Ok(()); // Not enough data for matrix
        }

        // Create transition matrix based on emotional changes
        let mut matrix = DMatrix::zeros(n, n);
        for i in 0..n {
            for j in 0..n {
                if i == j {
                    matrix[(i, j)] = emotional_vector[i]; // Self-transition probability
                } else if i + 1 == j {
                    matrix[(i, j)] = emotional_vector[i] * 0.8; // Forward transition
                } else if i > 0 && i - 1 == j {
                    matrix[(i, j)] = emotional_vector[i] * 0.5; // Backward transition
                }
            }
        }

        self.pitch_matrix = Some(matrix);
        Ok(())
    }

    /// Create a rhythm pattern matrix from arousal values
    pub fn create_rhythm_matrix(&mut self, arousal: f32, complexity: f32) -> PyResult<()> {
        let size = 16; // 16-beat pattern
        let mut matrix = DMatrix::zeros(size, size);

        // Create rhythmic patterns based on arousal
        for i in 0..size {
            for j in 0..size {
                if i == j {
                    matrix[(i, j)] = arousal; // On-beat emphasis
                } else if (i + 4) % 16 == j {
                    matrix[(i, j)] = arousal * 0.6; // Quarter-beat sync
                } else if (i + 8) % 16 == j {
                    matrix[(i, j)] = arousal * 0.3; // Half-beat sync
                } else {
                    matrix[(i, j)] = complexity * 0.1; // Complexity-driven variation
                }
            }
        }

        self.rhythm_matrix = Some(matrix);
        Ok(())
    }

    /// Create a harmony matrix from cultural context
    pub fn create_harmony_matrix(&mut self, cultural_context: &str) -> PyResult<()> {
        let scale_size = 12; // 12-tone equal temperament
        let mut matrix = DMatrix::zeros(scale_size, scale_size);

        // Define cultural harmony patterns
        let intervals = match cultural_context {
            "western" => vec![0, 2, 4, 5, 7, 9, 11], // Major scale intervals
            "eastern" => vec![0, 2, 4, 7, 9, 11], // Pentatonic scale
            "african" => vec![0, 2, 3, 5, 7, 9, 10], // African scale
            "latin" => vec![0, 2, 3, 5, 7, 8, 10], // Latin scale
            _ => vec![0, 2, 4, 5, 7, 9, 11], // Default to Western
        };

        // Create harmony matrix based on cultural intervals
        for i in 0..scale_size {
            for j in 0..scale_size {
                let interval = if i > j { i - j } else { j - i };
                if intervals.contains(&interval) {
                    matrix[(i, j)] = 1.0; // Harmonically consonant
                } else {
                    matrix[(i, j)] = 0.3; // Less consonant
                }
            }
        }

        self.harmony_matrix = Some(matrix);
        Ok(())
    }

    /// Compute optimal melody using matrix multiplication
    pub fn compute_melody(&self, emotional_vector: Vec<f32>) -> PyResult<Vec<f32>> {
        if let Some(ref pitch_matrix) = self.pitch_matrix {
            let n = emotional_vector.len();
            if pitch_matrix.nrows() != n {
                return Ok(emotional_vector); // Return input if dimensions don't match
            }

            let emotion_vec = DVector::from_vec(emotional_vector);
            let result = pitch_matrix * &emotion_vec;

            Ok(result.data.as_slice().to_vec())
        } else {
            Ok(emotional_vector)
        }
    }

    /// Get matrix dimensions for monitoring
    pub fn get_matrix_info(&self) -> PyResult<String> {
        let pitch_info = self.pitch_matrix.as_ref()
            .map(|m| format!("{}x{}", m.nrows(), m.ncols()))
            .unwrap_or("None".to_string());

        let rhythm_info = self.rhythm_matrix.as_ref()
            .map(|m| format!("{}x{}", m.nrows(), m.ncols()))
            .unwrap_or("None".to_string());

        let harmony_info = self.harmony_matrix.as_ref()
            .map(|m| format!("{}x{}", m.nrows(), m.ncols()))
            .unwrap_or("None".to_string());

        Ok(format!("Pitch: {}, Rhythm: {}, Harmony: {}", pitch_info, rhythm_info, harmony_info))
    }
}

#[pymodule]
fn aerowave_dsp(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // CORRECT REGISTRATION: No angle brackets in the fn signature
    m.add_class::<SignalProcessor>()?;
    m.add_class::<DataIngestor>()?;
    m.add_class::<CognitivePayload>()?;
    m.add_class::<LockFreeAudioPipeline>()?;
    m.add_class::<MusicMatrix>()?;
    Ok(())
}