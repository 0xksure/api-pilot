# API Assistant

## Local setup

In order to get started with the `cli-chat` you need to have python >= 3.12 installed and install the `requirement.txt`. The project is using [setuptools](https://setuptools.pypa.io/en/latest/userguide/quickstart.html) to build the project based on the [`pyproject.toml`](/cli-chat/pyproject.toml) 

## Requirements
- python >=3.12
- pip install -r `requirement.txt`
- Install cargo:
    
    ```
    > curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    ```
    Cargo for other platforms
    ```
    > https://forge.rust-lang.org/infra/other-installation-methods.html
    ```

## Install locally

```
    > pip install --editable .
    > api-chat --swagger ../idls/swagger/swagger.json
```

## FAQ
### Symlink to python3.12
```
> ln -sf /usr/local/bin/python3.12 /usr/local/bin/python3
```

# l; vblsf''hh\''ssaLPYT 3YODPZ`PNVCXZSFJL;]\;'`