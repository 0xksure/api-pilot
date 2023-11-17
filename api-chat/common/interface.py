
from common.utils import func_name_to_path
from result import Err,Ok,Result
from common.request import Request,Requests

import logging



"""
    Interface for assistant 
"""
class AssistantInterface:
    client = None
    id: str = None
    thread_id: str = None
    logger: logging.Logger = None

    def __init__(self, client,assistant_id: str, thread_id: str,logger: logging.Logger):
        self.id = assistant_id
        self.thread_id = thread_id
        self.client = client
        self.logger = logger
    
    def setup_assistant(key: str, assistant_instructions: str, function_json: dict) -> None:
        pass

    def run_assistant(self, task: str) -> Result[Requests,str]:
        pass