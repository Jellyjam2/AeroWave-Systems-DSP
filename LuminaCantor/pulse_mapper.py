"""
Pulse Mapper - Bio-Signal Integration Module
Maps heart-rate and biometric data from Project_Aegis_Core to SAT solver constraints
Integrates with postcard binary bridge for real-time bio-feedback music generation
"""

import time
import random
from typing import Dict, List, Optional, Tuple
from .postcard_bridge import PostcardBinaryBridge


class PulseMapper:
    """
    Bio-signal mapper that translates physiological data into musical parameters.
    Enables closed-loop bio-feedback systems for therapeutic music generation.
    """
    
    def __init__(self):
        """Initialize pulse mapper with postcard bridge."""
        self.postcard_bridge = PostcardBinaryBridge()
        self.baseline_bpm = 70.0  # Normal resting heart rate
        self.current_bpm = 70.0
        self.hrv_history: List[float] = []  # Heart rate variability history
        self.stress_level = 0.0  # 0.0 to 1.0 stress indicator
        self.anxiety_detected = False
        self.calibration_samples = 0
        self.calibrated = False
    
    def ingest_heart_rate(self, bpm: float, timestamp: Optional[float] = None) -> Dict[str, float]:
        """
        Process incoming heart rate data and compute biometric metrics.
        
        Args:
            bpm: Heart rate in beats per minute
            timestamp: Optional timestamp for data point
            
        Returns:
            Dictionary with processed biometric metrics
        """
        if timestamp is None:
            timestamp = time.time()
        
        self.current_bpm = bpm
        
        # Compute heart rate variability (simulated)
        if len(self.hrv_history) > 0:
            hrv = abs(bpm - self.hrv_history[-1])
            self.hrv_history.append(hrv)
            if len(self.hrv_history) > 30:
                self.hrv_history.pop(0)
        else:
            self.hrv_history.append(0.0)
        
        # Compute stress level based on BPM deviation from baseline
        bpm_deviation = abs(bpm - self.baseline_bpm) / self.baseline_bpm
        self.stress_level = min(1.0, bpm_deviation * 2.0)
        
        # Detect anxiety spike (rapid BPM increase)
        if len(self.hrv_history) >= 5:
            recent_hrv = sum(self.hrv_history[-5:]) / 5
            if recent_hrv > 10.0 and bpm > 90:
                self.anxiety_detected = True
            else:
                self.anxiety_detected = False
        
        return {
            'bpm': bpm,
            'stress_level': self.stress_level,
            'hrv': self.hrv_history[-1] if self.hrv_history else 0.0,
            'anxiety_detected': self.anxiety_detected,
            'timestamp': timestamp
        }
    
    def calibrate_baseline(self, bpm_samples: List[float]) -> bool:
        """
        Calibrate baseline heart rate from sample data.
        
        Args:
            bpm_samples: List of BPM samples for calibration
            
        Returns:
            True if calibration successful
        """
        if len(bpm_samples) < 10:
            return False
        
        self.baseline_bpm = sum(bpm_samples) / len(bpm_samples)
        self.calibrated = True
        self.calibration_samples = len(bpm_samples)
        
        return True
    
    def map_pulse_to_sat_constraints(self, biometric_data: Dict[str, float]) -> List[int]:
        """
        Convert biometric data into SAT solver constraints.
        
        Args:
            biometric_data: Dictionary with biometric metrics
            
        Returns:
            List of SAT clause values derived from biometric data
        """
        bpm = biometric_data.get('bpm', 70.0)
        stress_level = biometric_data.get('stress_level', 0.0)
        anxiety_detected = biometric_data.get('anxiety_detected', False)
        
        clauses = []
        
        # Constraint 1: BPM-based tempo mapping
        if bpm < 60:
            # Slow tempo - relaxing music
            clauses.extend([1, 2, 3])  # Low tempo constraints
        elif bpm > 100:
            # Fast tempo - energizing music
            clauses.extend([10, 11, 12])  # High tempo constraints
        else:
            # Normal tempo
            clauses.extend([5, 6, 7])  # Medium tempo constraints
        
        # Constraint 2: Stress level modulation
        if stress_level > 0.7:
            # High stress - calming constraints
            clauses.extend([-1, -2, -3])  # Reduce intensity
        elif stress_level < 0.3:
            # Low stress - energizing constraints
            clauses.extend([1, 2, 3])  # Increase intensity
        
        # Constraint 3: Anxiety override (highest priority)
        if anxiety_detected:
            # Emergency calming protocol
            clauses.extend([-10, -20, -30])  # Force calming
            clauses.append(0)  # Reset to baseline
        
        # Constraint 4: HRV-based complexity
        hrv = biometric_data.get('hrv', 0.0)
        if hrv > 15.0:
            # High variability - complex patterns
            clauses.extend([4, 8, 12])  # Increase complexity
        elif hrv < 5.0:
            # Low variability - simple patterns
            clauses.extend([-4, -8, -12])  # Reduce complexity
        
        return clauses
    
    def generate_bio_feedback_packet(self, biometric_data: Dict[str, float], 
                                     cultural_context: str = 'western') -> bytes:
        """
        Generate postcard binary packet with bio-feedback data.
        
        Args:
            biometric_data: Dictionary with biometric metrics
            cultural_context: Cultural context for music generation
            
        Returns:
            Binary packet for Rust backend
        """
        # Map biometric data to cognitive parameters
        stress_level = biometric_data.get('stress_level', 0.0)
        arousal = min(1.0, biometric_data.get('bpm', 70.0) / 120.0)  # Normalize BPM to arousal
        sentiment = 1.0 - stress_level  # Higher stress = lower sentiment
        
        # Map cultural context to ID
        culture_id_map = {
            'western': 0,
            'eastern': 1,
            'african': 2,
            'latin': 3
        }
        culture_id = culture_id_map.get(cultural_context, 0)
        
        # Generate SAT constraints from biometric data
        sat_clauses = self.map_pulse_to_sat_constraints(biometric_data)
        
        # Serialize to binary using postcard bridge
        binary_packet = self.postcard_bridge.serialize_cognitive_packet(
            sentiment, arousal, culture_id, sat_clauses
        )
        
        return binary_packet
    
    def get_therapeutic_recommendation(self, biometric_data: Dict[str, float]) -> Dict[str, any]:
        """
        Generate therapeutic music recommendations based on biometric state.
        
        Args:
            biometric_data: Dictionary with biometric metrics
            
        Returns:
            Dictionary with therapeutic recommendations
        """
        bpm = biometric_data.get('bpm', 70.0)
        stress_level = biometric_data.get('stress_level', 0.0)
        anxiety_detected = biometric_data.get('anxiety_detected', False)
        
        recommendations = {
            'target_bpm': 60.0,  # Calming target
            'tempo_bpm': 60,
            'key_mode': 'major',
            'complexity': 0.5,
            'instrumentation': 'soft',
            'intervention_needed': False
        }
        
        # Anxiety intervention protocol
        if anxiety_detected:
            recommendations.update({
                'target_bpm': 60.0,
                'tempo_bpm': 60,
                'key_mode': 'major',
                'complexity': 0.3,
                'instrumentation': 'ambient',
                'intervention_needed': True,
                'intervention_type': 'anxiety_calm'
            })
        # High stress protocol
        elif stress_level > 0.7:
            recommendations.update({
                'target_bpm': 65.0,
                'tempo_bpm': 70,
                'key_mode': 'major',
                'complexity': 0.4,
                'instrumentation': 'soft_piano',
                'intervention_needed': True,
                'intervention_type': 'stress_reduction'
            })
        # Low energy protocol
        elif bpm < 55:
            recommendations.update({
                'target_bpm': 75.0,
                'tempo_bpm': 80,
                'key_mode': 'major',
                'complexity': 0.6,
                'instrumentation': 'uplifting',
                'intervention_needed': True,
                'intervention_type': 'energy_boost'
            })
        
        return recommendations
    
    def simulate_project_aegis_stream(self, duration_seconds: float = 10.0) -> List[Dict[str, float]]:
        """
        Simulate bio-signal stream from Project_Aegis_Core for testing.
        
        Args:
            duration_seconds: Duration of simulation
            
        Returns:
            List of biometric data points
        """
        data_stream = []
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            # Simulate realistic heart rate patterns
            base_bpm = 70.0 + random.uniform(-5, 5)
            
            # Add stress spikes
            if random.random() < 0.1:
                base_bpm += random.uniform(20, 40)  # Stress spike
            
            # Add anxiety episodes
            if random.random() < 0.05:
                base_bpm += random.uniform(30, 50)  # Anxiety spike
            
            bpm = max(45, min(150, base_bpm))
            
            biometric_data = self.ingest_heart_rate(bpm)
            data_stream.append(biometric_data)
            
            time.sleep(0.1)  # 10Hz sampling rate
        
        return data_stream


class BioFeedbackLoop:
    """
    Closed-loop bio-feedback system for therapeutic music generation.
    Continuously monitors biometric signals and adjusts music parameters.
    """
    
    def __init__(self):
        """Initialize bio-feedback loop."""
        self.pulse_mapper = PulseMapper()
        self.active = False
        self.target_bpm = 70.0
        self.intervention_history: List[Dict] = []
    
    def start_feedback_loop(self, initial_bpm: float = 70.0) -> bool:
        """
        Start the bio-feedback loop.
        
        Args:
            initial_bpm: Initial heart rate for calibration
            
        Returns:
            True if loop started successfully
        """
        self.pulse_mapper.calibrate_baseline([initial_bpm] * 10)
        self.active = True
        return True
    
    def process_biometric_sample(self, bpm: float) -> Dict[str, any]:
        """
        Process a single biometric sample and generate music adjustments.
        
        Args:
            bpm: Heart rate in beats per minute
            
        Returns:
            Dictionary with music adjustments and recommendations
        """
        if not self.active:
            return {'error': 'Feedback loop not active'}
        
        # Process biometric data
        biometric_data = self.pulse_mapper.ingest_heart_rate(bpm)
        
        # Generate therapeutic recommendations
        recommendations = self.pulse_mapper.get_therapeutic_recommendation(biometric_data)
        
        # Generate bio-feedback packet
        binary_packet = self.pulse_mapper.generate_bio_feedback_packet(biometric_data)
        
        # Record intervention if needed
        if recommendations.get('intervention_needed'):
            self.intervention_history.append({
                'timestamp': time.time(),
                'bpm': bpm,
                'intervention_type': recommendations.get('intervention_type'),
                'packet_size': len(binary_packet)
            })
        
        return {
            'biometric_data': biometric_data,
            'recommendations': recommendations,
            'binary_packet': binary_packet,
            'packet_size': len(binary_packet)
        }
    
    def get_intervention_history(self) -> List[Dict]:
        """
        Get history of therapeutic interventions.
        
        Returns:
            List of intervention records
        """
        return self.intervention_history
    
    def stop_feedback_loop(self) -> bool:
        """
        Stop the bio-feedback loop.
        
        Returns:
            True if loop stopped successfully
        """
        self.active = False
        return True
