
from common.utils import func_name_to_path
from result import Err,Ok,Result
import requests


"""
    Request is a wrapper around the requests library.
"""
class Request:
    def __init__(self, request_type:str,path: str, arguments: dict):
        self.request_type = request_type
        self.path = path
        self.arguments = arguments

    def send(self,host: str) -> Result[requests.Response,str]:
        abs_url = host+self.path 
        if self.request_type == "GET":
            return Ok(requests.get(abs_url))
        elif self.request_type == "POST":
            return Ok(requests.post(abs_url, params=self.arguments))
        else:
            return Err("Invalid request type: "+self.request_type)
        
    def send_and_get_json(self,host: str) -> Result[dict,str]:
        response = self.send(host)
        if response.is_err():
            return Err(response.err())
        return Ok(response.unwrap().json())



"""
    Requests is a "list" of requests.
"""
class Requests:
    def __init__(self):
        self.requests: list[Request] = []
    
    def append(self,request: Request):
        self.requests.append(request)

    def send(self,host) -> Result[list[requests.Response],str]:
        responses = []
        for request in self.requests:
            response = request.send(host)
            if response.is_err():
                return Err(response.err())
            responses.append(response.unwrap())
        return Ok(responses)
    
    def send_and_get_json(self,host) -> Result[list[dict],str]:
        responses = []
        for request in self.requests:
            response = request.send_and_get_json(host)
            if response.is_err():
                return Err(response.err())
            responses.append(response.unwrap())
        return Ok(responses)

