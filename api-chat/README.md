# API Assistant

The API assistant is a [ChatGPT assistant](https://platform.openai.com/docs/assistants/overview) on top of an OpenAI IDL json file.
The CLI will based on prompts find the correct request and send it with the provided arguments. 

You can run the CLI from your terminal with
```bash
api-chat --idl=<OPENAI_IDL_PATH>
```

## Installation
The tool is available at [pypi](https://pypi.org/project/api-assistant/) and can be installed using pip
```bash
pip install api-assistant
```
### Extra - convert a swagger to OpenAI IDL
If you have generated a swagger (OpenAPI) for you API then you can use the s2o (swagger to openai) tool to convert it to a OpenAI IDL format. The tool can be installed with the cargo CLI that follows the [rust](https://www.rust-lang.org/learn/get-started) installation. 

If you have cargo installed then you can install it with
```bash
cargo install s2o
```

In order to interact with the cli there are some environment variables that needs to be present.

## Environment variables - REQUIRED

- OPENAI_API_KEY<string>: An OpenAI api key
- HOST<string>: The host of the API that you wish to query. Ex: http://localhost:8000
- ASSISTANT_INSTRUCTIONS<string>: A description (prompt) to the assistant of its purpose. Ex: For a payments api a typical instruction could be "ou are a wrapper around a payments api. Use the provided endpoints to answer user questions. Sometimes functions has to be combined to achieve the intended result."

## CLI Arguments
There is only one argument to the CLI itself 
- idl<string>: The path to the OpenAI IDL json. Ex: `api-chat --idl=./idls/openai.idl`.
