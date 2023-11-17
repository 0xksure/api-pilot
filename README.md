# API Assistant

The project allows you to interact with you API through prompts. 

# Setup 

## 1. Install s2o 
Either from crates
```
cargo install s2o
```
or from source
```
cd swagger_to_openai
cargo run 
```

If you have a swagger file then you can convert it to the OpenAPI IDL json by running
```
s2o convert swagger.json openai.json
```

The `openai.json` file can then be pointed to by the API assistant. 

## 2. Install the API assistant 
You can install the [API assistant](https://pypi.org/project/api-assistant/) using pip. Install the tool by running
```
pip install api-assistant
```

Read more about the tool and required environment variable [here](./src/README.md) 

## 3. Start interacting your API

Assuming you have a `openai.json` file and your web server is running at `printenv | grep HOST` you can interact with it using OpenAI 
```
api-chat --idl=openai.json
```
Good luck. 

# Support
Please file an issue if any of the above operations fails and we will support you as soon as possible.

# Package usage
It is also possible to use the package headless. The package contains a simple interface that an `OpenAIAssistance` class implements. It is possible to wrap this class in your own CLI or API if you want. 