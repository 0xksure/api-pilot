# start api 
start_api:
    docker-compose up --build -d

# generate swagger for api
generate_swagger:
    cd mock-api && swag init -g main.go

# convert swagger to openapi format
listen_to_swagger:
    cd swagger_to_openai && RUST_LOG=debug cargo run listen ../mock-api/docs ../idls/openai/


# interact with openapi
chat: 
    source .env && \
    source assistant/bin/activate && \
    python src/main.py --log=DEBUG

start: start_api generate_swagger chat
    
build_py:
    cd api-chat &&  python3 -m build --wheel && \
    python3 -m build --sdist

deploy_py: build_py
    cd api-chat && twine upload dist/*

build_s2o:
    cd swagger_to_openai && cargo build --release

deploy_s2o: build_s2o
    cd swagger_to_openai && cargo publish

create_env:
    python3 -m venv assistant