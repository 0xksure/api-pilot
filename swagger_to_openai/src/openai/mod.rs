use std::{
    collections::HashMap,
    fs::File,
    io::{Error, Write},
};

use serde;

use crate::swagger::swagger2::Swagger;
/// Contains specs for the openai function struct
/// Ex:
/*
{
    "type": "function",
    "function": {
    "name": "GetBalance",
    "description": "Gets the balance of the users account",
    "parameters": {
        "type": "object",
        "properties": {
        "userId": {"type": "string", "description": "The user id of the user. It is unique"},
        },
        "required": ["userId"]
    }
    }
},
{
    "type": "function",
    "function": {
        "name": "TransferAmount",
        "description": "Transfers amount from one account to another",
        "parameters": {
            "type": "object",
            "properties": {
                "fromUserId": {"type": "string", "description": "The user id of the sender. It is unique"},
                "toUserId": {"type": "string", "description": "The user id of the receiver. It is unique"},
                "amount": {"type": "number", "description": "The amount to transfer"}
            },
            "required": ["fromUserId","toUserId","amount"]
        }
    }
},
    {
    "type": "function",
    "function": {
    "name": "GetUserId",
    "description": "Gets the user id from the user name",
    "parameters": {
        "type": "object",
        "properties": {
        "userName": {"type": "string", "description": "This is the unique user name of the user"},
        },
        "required": ["userName"]
    }
    }
}
*/

#[derive(serde::Serialize, Debug)]
pub struct OpenAIFuncProperty {
    #[serde(rename = "type")]
    pub property_type: String,
    pub description: String,
}

#[derive(serde::Serialize, Debug)]
pub struct OpenAIFuncParams {
    #[serde(rename = "type")]
    pub func_type: String,
    pub properties: Option<HashMap<String, OpenAIFuncProperty>>,
    pub required: Vec<String>,
}

#[derive(serde::Serialize, Debug)]
pub struct OpenAIFunctionSpec {
    pub name: String,
    pub description: String,
    pub parameters: OpenAIFuncParams,
}

#[derive(serde::Serialize, Debug)]
pub struct OpenAIFunction {
    #[serde(rename = "type")]
    pub object_type: String,
    pub function: OpenAIFunctionSpec,
}

pub type OpenAIFunctions = Vec<OpenAIFunction>;

pub fn gen_openaifunctions_from_swagger(
    swagger: Swagger,
) -> Result<OpenAIFunctions, serde_json::Error> {
    let mut openai_functions: Vec<OpenAIFunction> = Vec::new();
    for (path_key, path_item) in swagger.paths {
        for (method, path) in path_item {
            let parameters: Option<HashMap<String, OpenAIFuncProperty>>;
            let mut required_params = Vec::new();
            if path.parameters.len() == 0 {
                parameters = None;
            } else {
                let mut params = HashMap::new();
                for parameter in path.parameters {
                    params.insert(
                        parameter.name.clone(),
                        OpenAIFuncProperty {
                            property_type: parameter.path_param_type,
                            description: parameter.description,
                        },
                    );
                    let parameter_name = parameter.name;
                    log::debug!("Parameter: {:?} {:?}", &parameter_name, parameter.required);
                    if parameter.required {
                        required_params.push(parameter_name);
                    }
                }
                parameters = Some(params);
            }

            // generate FunctionName
            let path_as_camel_case = path_key
                .split("/")
                .map(|s| {
                    let s_stripped = s.replace("{", "").replace("}", "");
                    let mut c = s_stripped.chars();
                    match c.next() {
                        None => String::new(),
                        Some(f) => format!("_{}{}", f, c.as_str()),
                    }
                })
                .collect::<Vec<String>>()
                .join("");
            let func_name = format!("{}{}", method, path_as_camel_case);
            let openai_function = OpenAIFunction {
                object_type: "function".to_string(),
                function: OpenAIFunctionSpec {
                    name: func_name,
                    description: format!("{}. {}", path.summary, path.description),
                    parameters: OpenAIFuncParams {
                        func_type: "object".to_string(),
                        properties: parameters,
                        required: required_params,
                    },
                },
            };
            openai_functions.push(openai_function);
        }
    }

    Ok(openai_functions)
}

pub trait OpenAIFunctionsTrait {
    fn write_to_json_file(&self, path: &str) -> Result<(), Error>;
    fn write_to_string(&self) -> Result<String, Error>;
}

impl OpenAIFunctionsTrait for OpenAIFunctions {
    fn write_to_json_file(&self, path: &str) -> Result<(), Error> {
        let serialized_data = serde_json::to_string(&self).unwrap();
        let mut out_file = File::create(path).unwrap();
        return out_file.write_all(serialized_data.as_bytes());
    }

    fn write_to_string(&self) -> Result<String, Error> {
        let serialized_data = serde_json::to_string(&self).unwrap();
        return Ok(serialized_data);
    }
}
