use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use html2md::parse_html;


#[pyfunction]
fn html_to_md(html: &str) -> String {
    parse_html(html)
}

#[pymodule]
fn rhtml2text(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(html_to_md))?;
    Ok(())
}
