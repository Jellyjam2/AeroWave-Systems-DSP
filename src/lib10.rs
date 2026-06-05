use pyo3::prelude::*;
use std::time::Instant;
use rayon::prelude::*;
use rand::prelude::*;
use std::sync::Arc;

#[pyclass]
pub struct TitanGeneral {
    #[pyo3(get, set)]
    pub weights: Vec<f32>,
    pub heat_map: Vec<usize>,
}

#[pymethods]
impl TitanGeneral {
    #[new]
    fn new() -> Self {
        TitanGeneral { weights: Vec::new(), heat_map: Vec::new() }
    }

    // PROJECT 1: THE WATCH-FORGE (LOGIC)
    fn solve_php_strike(&self, p: i32) -> PyResult<(bool, f64, usize)> {
        let start = Instant::now();
        let h = p - 1;
        let num_vars = p * h;
        let mut assignment = vec![false; (num_vars + 1) as usize];
        let mut checks = 0;
        for v in 1..=num_vars {
            assignment[v as usize] = true;
            let p_idx = (v - 1) / h;
            let h_idx = (v - 1) % h;
            for other_p in 0..p {
                if other_p == p_idx { continue; }
                checks += 1;
                let other_v = (other_p * h) + h_idx + 1;
                if assignment[other_v as usize] {
                    return Ok((false, start.elapsed().as_secs_f64(), checks));
                }
            }
        }
        Ok((true, start.elapsed().as_secs_f64(), checks))
    }

    // PROJECT 2: THE EXORCIST (HEAT)
    fn isolate_hot_core(&mut self, clauses: Vec<Vec<i32>>, vars: usize, steps: usize) -> PyResult<(Vec<usize>, f64)> {
        let start = Instant::now();
        let shared_clauses = Arc::new(clauses);
        let results: Vec<Vec<usize>> = (0..4).into_par_iter().map(|seed| {
            let mut rng = StdRng::seed_from_u64(seed as u64);
            let mut assignment = vec![rng.gen_bool(0.5); vars + 1];
            let mut local_heat = vec![0; shared_clauses.len()];
            for _ in 0..steps {
                let v = rng.gen_range(1..=vars);
                assignment[v] = !assignment[v];
                for (idx, c) in shared_clauses.iter().enumerate() {
                    let mut sat = false;
                    for &lit in c { if assignment[lit.abs() as usize] == (lit > 0) { sat = true; break; } }
                    if !sat { local_heat[idx] += 1; }
                }
            }
            local_heat
        }).collect();
        self.heat_map = vec![0; shared_clauses.len()];
        for map in results { for (i, &val) in map.iter().enumerate() { self.heat_map[i] += val; } }
        Ok((self.heat_map.clone(), start.elapsed().as_secs_f64()))
    }
}

#[pymodule]
fn titan_forge(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<TitanGeneral>()?;
    Ok(())
}