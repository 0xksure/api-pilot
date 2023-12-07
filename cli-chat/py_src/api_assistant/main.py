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
@click.option('--swagger',
        prompt="The swagger json file",
        help="The swagger json file generated from your api code",
        type=click.Path(exists=True))
def main(swagger):
    config = utils.get_config()

    function_json = json.loads(s2opy.swagger_from_file(swagger))
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