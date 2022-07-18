use pyo3::prelude::*;
use std::path::PathBuf;
//use std::io;
mod cst_exports;
use cst_exports::cst_find_exports::*;

/// Python test function
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a+b).to_string())
}

#[pyfunction]
fn cst_exports_list(path: String) -> PyResult<Vec<String>> {
    let exports = cst_find_exports(PathBuf::from(path))
                    .unwrap()
                    .iter()
                    .map(|e| e.to_string_lossy().to_string())
                    .collect::<Vec<_>>();

    Ok(exports)
}

/// Python cstutils module
#[pymodule]
fn cstutil_rs(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(cst_exports_list, m)?)?;
    Ok(())
}

