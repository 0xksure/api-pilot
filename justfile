# start api 
start_api:
    docker-compose up --build -d

# generate swagger for api
generate_swagger:
    cd cmd && swag init -g main.go

# convert swagger to openapi format
listen_to_swagger:
    cd swagger_to_openai && RUST_LOG=debug cargo run listen ../cmd/docs ../idls/openai/


# interact with openapi
chat: 
    source .env && \
    source assistant/bin/activate && \
    python src/main.py --log=DEBUG

start: start_api generate_swagger chat
    