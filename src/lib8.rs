use pyo3::prelude::*;
use rayon::prelude::*;
use rand::prelude::*;
use std::time::Instant;
use std::sync::Arc;

#[pyclass]
pub struct OmegaAnnealer {
    pub vars: usize,
}

#[pymethods]
impl OmegaAnnealer {
    #[new]
    fn new(vars: usize) -> Self { OmegaAnnealer { vars } }

    fn execute_omega_siege(&self, clauses: Vec<Vec<i32>>, steps: usize) -> PyResult<(bool, usize, f64)> {
        let start = Instant::now();
        let vars = self.vars;
        
        // Wrap clauses in Arc so all 4 i3-threads can read it safely
        let shared_clauses = Arc::new(clauses);

        // QUAD-BLADE: Parallel execution
        let results: Vec<usize> = (0..4).into_par_iter().map(|thread_id| {
            let mut rng = StdRng::seed_from_u64(thread_id as u64 + 42);
            let mut assignment = vec![false; vars + 1];
            for v in 1..=vars { assignment[v] = rng.gen(); }

            let local_clauses = Arc::clone(&shared_clauses);
            let mut current_energy = calculate_energy_internal(&local_clauses, &assignment);
            let mut temp: f64 = 100.0;
            let mut best_energy = current_energy;
            let mut stuck_counter = 0;

            for _ in 0..steps {
                if current_energy == 0 { return 0; }

                let v = rng.gen_range(1..=vars);
                assignment[v] = !assignment[v];
                let new_energy = calculate_energy_internal(&local_clauses, &assignment);

                if new_energy < current_energy || rng.gen_bool((-(new_energy as f64 - current_energy as f64) / temp).exp().min(1.0)) {
                    current_energy = new_energy;
                    if current_energy < best_energy {
                        best_energy = current_energy;
                        stuck_counter = 0;
                    }
                } else {
                    assignment[v] = !assignment[v];
                }

                stuck_counter += 1;
                if stuck_counter > 100_000 {
                    temp = 50.0; // PHOENIX REHEAT
                    stuck_counter = 0;
                } else {
                    temp *= 0.999995;
                }
            }
            best_energy
        }).collect();

        let absolute_best = *results.iter().min().unwrap();
        Ok((absolute_best == 0, absolute_best, start.elapsed().as_secs_f64()))
    }
}

// Helper function outside the class to allow thread-safe sharing
fn calculate_energy_internal(clauses: &[Vec<i32>], assignment: &[bool]) -> usize {
    let mut energy = 0;
    for c in clauses {
        let mut sat = false;
        for &lit in c {
            let var = lit.abs() as usize;
            if assignment[var] == (lit > 0) { sat = true; break; }
        }
        if !sat { energy += 1; }
    }
    energy
}

#[pymodule]
fn titan_forge(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<OmegaAnnealer>()?;
    Ok(())
}