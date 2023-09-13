use pyo3::{exceptions::PyValueError, prelude::*, types::PyBytes, wrap_pyfunction};

use fea_rs::{
    compile::{error::CompilerError, Opts},
    Compiler, GlyphMap, GlyphName,
};

#[pymodule]
fn notabug(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(compile_from_file))?;
    Ok(())
}

fn compiler_err_to_py_err(error: CompilerError) -> PyErr {
    PyValueError::new_err(format!("{}", error))
}

#[pyfunction]
fn compile_from_file(
    py: Python,
    root_path: String,
    glyph_order: Vec<String>,
) -> PyResult<&PyBytes> {
    let map: GlyphMap = glyph_order.iter().map(GlyphName::new).collect();
    Compiler::new(root_path, &map)
        .compile()
        .map_err(compiler_err_to_py_err)
        .and_then(|r| {
            r.to_binary(&map, Opts::default())
                .map_err(|_| PyValueError::new_err("Couldn't build binary"))
        })
        .map(|bytes| PyBytes::new(py, &bytes))
}
