import os 
import sys


def get_env_var(key):
    value = os.environ.get(key)
    if not value:
        print(f"Failed to get {key}")
        sys.exit(1)
    return value


def get_config():
    return {
        "host": get_env_var("HOST"),
        "assistant_instructions": get_env_var("ASSISTANT_INSTRUCTIONS"),
        "api_key": get_env_var("OPENAI_API_KEY"),
    }


"""
    func_name_to_path converts a function name to a path.

    Ex: 
    - get_balance -> GET /balance
    - post_balance -> POST /balance
    - get_balance_by_id -> GET /balance/by/id
"""
def func_name_to_path(func_name: str):
    parts = func_name.split("_")
    request_type = parts[0].upper()
    path = "/".join(parts[1:])
    return request_type, "/"+path


