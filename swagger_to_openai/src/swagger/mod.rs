use std::{
    collections::HashMap,
    env,
    fs::File,
    io::{Error, Read},
};

use serde::Deserialize;

#[derive(Deserialize, Debug)]
pub struct Response {
    pub description: String,
}

#[derive(Deserialize, Debug)]
pub struct PathParameters {
    #[serde(rename = "type")]
    pub path_param_type: String,
    pub description: String,
    pub name: String,
    #[serde(rename = "in")]
    pub _in: String,
    #[serde(default)]
    pub required: bool,
}

#[derive(Deserialize, Debug)]
pub struct Path {
    pub description: String,
    pub produces: Vec<String>,
    pub summary: String,
    pub parameters: Vec<PathParameters>,
    pub responses: HashMap<String, Response>,
}

#[derive(Deserialize, Debug)]
pub struct PathItem {
    pub methods: HashMap<String, Path>,
}

#[derive(Deserialize, Debug)]
pub struct Info {
    pub contact: HashMap<String, String>,
}

#[derive(Deserialize, Debug)]
pub struct Swagger {
    pub swagger: String,
    pub info: Info,
    pub paths: HashMap<String, HashMap<String, Path>>,
}

impl Swagger {
    pub fn from_json(json: &str) -> Result<Swagger, serde_json::Error> {
        serde_json::from_str::<Swagger>(&json)
    }

    pub fn from_file(path: &str) -> Result<Swagger, Error> {
        let relative_file_path = format!("{}/{}", std::env::current_dir().unwrap().display(), path);
        let mut swagger_file = match File::open(&relative_file_path) {
            Ok(file) => file,
            Err(e) => {
                log::error!(
                    "Error opening file {} with error {:?}",
                    relative_file_path,
                    e
                );
                return Err(e);
            }
        };
        let mut data = String::new();
        swagger_file.read_to_string(&mut data).unwrap();

        // load the swagger yaml
        Ok(Swagger::from_json(&data)?)
    }
}
