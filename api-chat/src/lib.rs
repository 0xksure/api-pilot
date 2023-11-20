use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::type_object::PyTypeInfo;
use s2o::openai::{gen_openaifunctions_from_swagger, OpenAIFunction};
use s2o::swagger::Swagger;

#[pyfunction]
fn swagger_from_file(path: &str) -> PyResult<Vec<OpenAIFunction>> {
    match Swagger::from_file(path) {
        Ok(swagger) => match gen_openaifunctions_from_swagger(swagger) {
            Ok(openaifunctions) => {
                println!("openaifunctions: {:?}", openaifunctions);
                Ok(openaifunctions)
            }
            Err(e) => Err(PyValueError::new_err(format!("Error: {}", e))),
        },
        Err(e) => Err(PyValueError::new_err(format!("Error: {}", e))),
    }
}

#[pymodule]
#[pyo3(name = "s2opy")]
fn s2opy(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(swagger_from_file, m)?)?;
    Ok(())
}
