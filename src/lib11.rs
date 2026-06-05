use pyo3::prelude::*;
use std::time::Instant;

#[pyclass]
pub struct AutoBlaster {
    pub manifold: Vec<Vec<i32>>,
}

#[pymethods]
impl AutoBlaster {
    #[new]
    fn new() -> Self {
        AutoBlaster { manifold: Vec::new() }
    }

    /// THE BIT-BLAST STRIKE: Unrolling an integer into logic gates
    fn blast_integer(&mut self, target: u64) -> PyResult<(usize, f64)> {
        let start = Instant::now();
        self.manifold.clear();
        
        let bits = 64 - target.leading_zeros();
        for i in 0..bits {
            let var = (i + 1) as i32;
            // If the bit at position i is set, the variable must be True
            if (target >> i) & 1 == 1 {
                self.manifold.push(vec![var]);
            } else {
                self.manifold.push(vec![-var]);
            }
        }
        
        let duration = start.elapsed().as_secs_f64();
        Ok((self.manifold.len(), duration))
    }
}

#[pymodule]
fn titan_forge(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<AutoBlaster>()?;
    Ok(())
}