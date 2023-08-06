#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pyfunction]
fn sum_as_string(a: i64, b: i64) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pymodule]
fn bergkvist_test(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(sum_as_string))?;
    Ok(())
}
