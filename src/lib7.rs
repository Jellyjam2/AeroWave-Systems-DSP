use pyo3::prelude::*;
use std::time::Instant;
use rand::{thread_rng, Rng}; // Explicitly importing the RNG traits

#[pyclass]
pub struct AnnealingForge {
    pub vars: usize,
}

#[pymethods]
impl AnnealingForge {
    #[new]
    fn new(vars: usize) -> Self { 
        AnnealingForge { vars } 
    }

    /// THE QUANTUM TUNNEL: Thermal Vibration via Metropolis-Hastings
    fn execute_tunnel_strike(&self, clauses: Vec<Vec<i32>>, steps: usize) -> PyResult<(bool, f64, f64)> {
        let start = Instant::now();
        let mut rng = thread_rng();
        let mut assignment = vec![false; self.vars + 1];
        
        let mut current_energy = clauses.len();
        let mut temperature: f64 = 100.0;
        let cooling_rate = 0.9995;

        for _ in 0..steps {
            if current_energy == 0 { break; }

            // Pick a random bit to 'Vibrate'
            let v = rng.gen_range(1..=self.vars);
            assignment[v] = !assignment[v];

            let mut new_energy = 0;
            for c in &clauses {
                let mut satisfied = false;
                for &lit in c {
                    let var = lit.abs() as usize;
                    if assignment[var] == (lit > 0) {
                        satisfied = true;
                        break;
                    }
                }
                if !satisfied { new_energy += 1; }
            }

            // Metropolis Logic: Jumping the Wall
            if new_energy < current_energy || rng.gen_bool((-(new_energy as f64 - current_energy as f64) / temperature).exp().min(1.0)) {
                current_energy = new_energy;
            } else {
                assignment[v] = !assignment[v]; // Revert the flip
            }

            temperature *= cooling_rate;
        }

        let success = current_energy == 0;
        let duration = start.elapsed().as_secs_f64();
        Ok((success, duration, current_energy as f64))
    }
}

#[pymodule]
fn titan_forge(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<AnnealingForge>()?;
    Ok(())
}