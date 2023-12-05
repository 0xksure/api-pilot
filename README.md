# API Chat
[![Crates.io](https://img.shields.io/crates/v/fuzzy-matcher.svg)](https://crates.io/crates/fuzzy-matcher)
[![PyPI - Version](https://img.shields.io/pypi/v/api-assistant)](https://pypi.org/project/api-assistant/)

Chat with your API! 

> Note: The swagger to OpenAI IDL conversion only supports swagger2. The implementation is found in [swagger_to_openai](/swagger_to_openai/README.md)



## Local usage 
To get started 

### Requirements
- OpenAI API key in [.env.example](/example.env) - OPENAI_API_KEY
- A swagger2 file.
- (optional) A web server to run the requests against - HOST
- (optional) Docker if you wish to run against the [mock-api](/mock-api/README.md)
- (optional) Rust if you wish to develop on the swagger to openai idl project (s2o).

### Setup

### 1. Set the Environment variables 
The necessary environment variables is defined in [.env.example](/example.env). 
2. Create a python >= 3.12 environement. 

### 2 Set up python virtual environment
In order to run the [cli-chat](/cli-chat/README.md) you need [python 3.12](https://www.python.org/downloads/) or later installed. Best practise is to create a virtual environment using commands `python3 -m venv assistant`. On unix systems it's possible to run `python3 --version` to get the current python3 version. If the version is below 3.12 you likely need to download it. If after installing the latest python3 you still get the old version when you run `python3 --version` then you need to symlink the `python3` version to the lastest download. This can be done like this
```
    > PYTHON_PATH=$(which python3.12)
    > ln -s $PYTHON_PATH /usr/bin/python3
```

There's also a [just](/justfile#35) recipe for creating a venv. 

### 3 Build and run project
Please follow the guide in the [cli-chat](/cli-chat/README.md) readme to get up and running. 

## Package usage
It is also possible to use the project without running it locally. This can be done by installing the [api-assistant](https://pypi.org/project/api-assistant/) using `pip`.

```
pip install api-assistant
```



## Interact with your API 

You are now ready to run the assistant against your swagger. 

An example is to generate a swagger from the [mock-api](/mock-api/README.md) and run it locally using `docker`.
```
    > api-chat --swagger ../idls/swagger_2/swagger.json
```

# Project structure

The project is structured in separate folder where some of the project depends on each other. The projects are

- 🚧 [api-chat](/api-chat/README.md): Exposes the api chat through a flask api. This is still under construction.  
- [swagger_to_openai](/swagger_to_openai/README.md): The engine that converts Swagger2 (OpenAPI) to the OpenAI IDL expected as input to the assistant. Note Swagger3 -> OpenAI IDL is still in 🚧
- [cli-chat](/cli-chat/README.md): Allows users to chat with a OpenAI IDL in the terminal. 
- [mock-api](/mock-api/README.md): A basic go rest api that can be used to generate swagger and also used as a web server for the cli chat. 
- [idls](/idls/): A scratch area for IDLs and Swaggers to be tested with the cli-chat.

# Support
Please file an issue if any of the above operations fails and we will support you as soon as possible.
