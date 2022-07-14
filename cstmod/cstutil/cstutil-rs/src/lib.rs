use pyo3::prelude::*;

/// Python test function
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a+b).to_string())
}

/// Python cstutils module
#[pymodule]
fn cstutil_rs(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
}

//#[cfg(test)]
//mod tests {
//    #[test]
//    fn it_works() {
//        let result = 2 + 2;
//        assert_eq!(result, 4);
//    }
//}
