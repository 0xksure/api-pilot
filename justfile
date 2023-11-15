
# start api 
start_api:
    go run cmd/api/main.go

# generate swagger for api
generate_swagger:
    swag init -g cmd/api/main.go

# prepares files for conversion
prepare_files:
    cp cmd/dock/swagger.json idls/swagger/swagger.json

# convert swagger to openapi format
convert_swagger:
    cd swagger_to_openai && RUST_LOG=debug cargo run generate ../idls/swagger/swagger.json ../idls/openai/openai.json

# interact with openapi
chat $prompt: 
    source assistant/bin/activate && \
    python src/main.py $prompt
