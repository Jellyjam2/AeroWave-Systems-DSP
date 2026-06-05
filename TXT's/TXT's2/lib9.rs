use pyo3::prelude::*;
use std::time::Instant;
use std::sync::Arc;
use rayon::prelude::*;
use rand::prelude::*;

#[pyclass]
pub struct ExorcistForge {
    pub vars: usize,
    pub heat_map: Vec<usize>, // Tracking the 'Hot' clauses
}

#[pymethods]
impl ExorcistForge {
    #[new]
    fn new(vars: usize, num_clauses: usize) -> Self {
        ExorcistForge { vars, heat_map: vec![0; num_clauses] }
    }

    /// THE EXORCISM: Annealing + Heat Mapping
    fn isolate_hot_core(&mut self, clauses: Vec<Vec<i32>>, steps: usize) -> PyResult<(Vec<usize>, f64)> {
        let start = Instant::now();
        let shared_clauses = Arc::new(clauses);
        let vars = self.vars;

        // Run a high-speed thermal probe to find the frustration points
        let results: Vec<Vec<usize>> = (0..4).into_par_iter().map(|seed| {
            let mut rng = StdRng::seed_from_u64(seed as u64);
            let mut assignment = vec![rng.gen_bool(0.5); vars + 1];
            let mut local_heat = vec![0; shared_clauses.len()];

            for _ in 0..steps {
                let v = rng.gen_range(1..=vars);
                assignment[v] = !assignment[v];
                
                for (idx, c) in shared_clauses.iter().enumerate() {
                    let mut sat = false;
                    for &lit in c {
                        if assignment[lit.abs() as usize] == (lit > 0) { sat = true; break; }
                    }
                    if !sat { local_heat[idx] += 1; }
                }
            }
            local_heat
        }).collect();

        // Combine Heat Maps into the Global Ledger
        for map in results {
            for (i, &val) in map.iter().enumerate() {
                self.heat_map[i] += val;
            }
        }

        Ok((self.heat_map.clone(), start.elapsed().as_secs_f64()))
    }
}

#[pymodule]
fn titan_forge(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<ExorcistForge>()?;
    Ok(())
}