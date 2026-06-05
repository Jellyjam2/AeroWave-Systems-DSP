use pyo3::prelude::*;
use varisat::{ExtendFormula, Solver};

#[pyclass]
pub struct Forge {
    #[pyo3(get)]
    pub clauses: Vec<Vec<i32>>,
    #[pyo3(get)]
    pub num_vars: i32,
}

#[pymethods]
impl Forge {
    #[new]
    fn new(clauses: Vec<Vec<i32>>, num_vars: i32) -> Self {
        Forge { clauses, num_vars }
    }

    fn solve_internal(&mut self) -> PyResult<Option<Vec<i32>>> {
        if self.clauses.is_empty() { return Ok(None); }
        let mut solver = Solver::new();
        for clause in &self.clauses {
            let lits: Vec<varisat::Lit> = clause.iter()
                .map(|&l| varisat::Lit::from_dimacs(l as isize)).collect();
            solver.add_clause(&lits);
        }
        match solver.solve() {
            Ok(true) => {
                let model = solver.model().unwrap();
                Ok(Some(model.iter().map(|&l| l.to_dimacs() as i32).collect()))
            }
            _ => Ok(None),
        }
    }
}

#[pymodule]
fn titan_forge(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Forge>()?;
    Ok(())
}
