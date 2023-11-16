# Prototype of crating prompts for APIs

The project allows you to interact with you API through prompts. 

# Setup 

## 1. Install s2o 
Either from crates
```
> cargo install s2o
```
or using the local code
```
> cd swagger_to_openai
> cargo run 
```

## Start interacting with the example api

```
>
```

## Workflow

1. work on you project and ouput a swagger.json
2. use the swagger_to_openai cli to convert the swagger to an openai idl
3. read the idl in the python script 
4. create a prompt -> openai will find the appropriate endpoint and call it 

```bash
    python src/main.py 
```
Will activate the assistant and lets you query you api through prompts!