use pyo3::prelude::*;
use std::collections::HashSet;

// --- THE LOGIC FURNACE (CDCL) ---

// Helper: Resolution Rule (Merging two clauses to find the root cause)
fn resolve(c1: Vec<i32>, c2: Vec<i32>, var: i32) -> Vec<i32> {
    let mut merged: HashSet<i32> = c1.into_iter().collect();
    for lit in c2 {
        merged.insert(lit);
    }
    merged.remove(&var);
    merged.remove(&(-var));
    merged.into_iter().collect()
}

// Helper: 1-UIP Check
fn is_1uip(clause: &[i32], current_lits: &HashSet<i32>) -> bool {
    clause.iter().filter(|&&l| current_lits.contains(&l.abs())).count() == 1
}

#[pyfunction]
fn forge_1uip(
    learnt: Vec<i32>, 
    trail: Vec<i32>, 
    reasons: Vec<Option<usize>>, 
    clauses: Vec<Vec<i32>>, 
    current_level_lits: HashSet<i32>
) -> PyResult<Vec<i32>> {
    let mut learnt_clause = learnt;
    let mut i = trail.len() as i32 - 1;

    while !is_1uip(&learnt_clause, &current_level_lits) && i >= 0 {
        let lit = trail[i as usize];
        if learnt_clause.contains(&(-lit)) {
            if let Some(reason_idx) = reasons[lit.abs() as usize] {
                let reason_clause = clauses[reason_idx].clone();
                learnt_clause = resolve(learnt_clause, reason_clause, lit.abs());
            }
        }
        i -= 1;
    }
    Ok(learnt_clause)
}

// --- THE STOCHASTIC EYES (ZEROIDS) ---

#[pyfunction]
fn zeroid_terrain_check(current_volume: f64, terrain_noise: Vec<f64>) -> PyResult<f64> {
    // 0.018 Gauss-Aligned Sampling: Navigating the 'Black-Box' without gradients
    let mut best_stability = f64::MAX;
    let mut optimized_v = current_volume;

    for &noise in &terrain_noise {
        // Zero-Order Logic: We don't calculate a slope, we find the resonance
        let stability = (current_volume + noise).abs() % 0.018; 
        if stability < best_stability {
            best_stability = stability;
            optimized_v = current_volume + noise;
        }
    }
    Ok(optimized_v)
}

// --- THE MODULE MANIFEST ---

#[pymodule]
fn titan_forge(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(forge_1uip, m)?)?;
    m.add_function(wrap_pyfunction!(zeroid_terrain_check, m)?)?;
    Ok(())
}
