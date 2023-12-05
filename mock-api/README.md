# Mock API

This is a mock API that can be used to test against the [cli-chat](/cli-chat/README.md). It is super basic and only contains a couple of endpoints that's annotated for Swagger 2 generation.

## Setup 

### Requirements
- Go installed locally 
- [swaggo/swag](https://github.com/swaggo/swag) installed to be used to convert the Swagger annotation to a `swagger.json` file. 
- Docker (nerdctl etc) if you want to run the web backend in docker. Also see the [just](/justfile#l3) recipe for running with docker.

To target the Go web backend with the [cli-chat](/cli-chat/README.md) please point the `--swagger` flag tp `mock-api/docs/swagger.json`. This will allow the [s2o](/swagger_to_openai/README.md) tool to convert the swagger to OpenAI IDL that is used by the AI.
