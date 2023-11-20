from openai import OpenAI
import os 
import time
import sys
import click
import json
import requests
import common.utils as utils
from common.interface import AssistantInterface
import api_assistant.s2opy as s2opy  

from oai.main import OpenAIAssistant
import logging

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)




# Main is the cli entrypoint
@click.command()
@click.option('--idl',
        prompt="The file location of the OpenAI IDL json",
        help="If you don't have a OpenAI IDL json then please install the s2o rust crate and convert your swagger.",
        type=click.Path(exists=True))
def main(idl):
    config = utils.get_config()


    function_json = s2opy.swagger_from_file("../idls/swagger/swagger.json")
    print("function_json: ", function_json)
    assistant = OpenAIAssistant.setup_assistant(config["api_key"],config["assistant_instructions"],function_json,logger)
    print("Welcome to the OpenAI API Wrapper")
    print("Type your question and press enter to get started")
    print("Type exit to exit")
    while True:
        prompt = input("> ")
        if prompt == "exit":
            print("Goodbye")
            break
        if prompt:
            task = prompt.strip()
            startTime = time.time()
            result = assistant.run_assistant(task)
            
            if result.is_err():
                print("Error with running the assistant: ",result)
                message = result.err()
                print(message)
                continue            
            else:
                logger.debug(f"Debugging: Total time taken: {time.time() - startTime}")
                request_list = result.unwrap()
                print("Sending requests: ", request_list)
                result = request_list.send_and_get_json(config["host"])
                if not result.is_err():
                    print("Responses are: ")
                    for r in result.unwrap():
                        print(r)
                    continue
                else:
                    print("Found no matching requests")
                    continue