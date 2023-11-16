from openai import OpenAI
import os 
import time
import sys
import click
import json
import requests
from enum import Enum
import logging

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

class Result(Enum):
    OK = 1
    ERROR = 2
    PROMPT = 3


def setup_assistant(client, task,assistant_instructions,function_json):
    # Load function json from file 
    logger.debug("Debugging: Function json is ", function_json)
    # create a new agent
    assistant = client.beta.assistants.create(
        instructions=assistant_instructions,
        model="gpt-4-1106-preview",
        tools=function_json
    )

    # Create a new thread
    thread = client.beta.threads.create()

    # Create a new thread message with the provided task
    client.beta.threads.messages.create(
        thread.id,
        role="user",
        content=task,
        )

    # Return the assistant ID and thread ID
    return assistant.id, thread.id




def run_assistant(client, assistant_id, thread_id):
    # Create a new run for the given thread and assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    # Loop until the run status is either "completed" or "requires_action"
    while run.status == "in_progress" or run.status == "queued":
        time.sleep(0.2)
        logger.debug("Debugging: Run status is ", run.status)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

        # At this point, the status is either "completed" or "requires_action"
        if run.status == "completed":
            return (Result.PROMPT,client.beta.threads.messages.list(
              thread_id=thread_id
            ),run.status,run.id)
        
        if run.status == "requires_action":
            logger.debug("Debugging: The run requires an action")
            logger.debug("Required actions: ",run.required_action)
            logger.info("Output: ", run.required_action.submit_tool_outputs.tool_calls)
           
            return  (Result.OK ,run.required_action.submit_tool_outputs.tool_calls,run.status,run.id)

    return (Result.ERROR, None,run.status,run.id)
            

def func_name_to_path(func_name: str):
    parts = func_name.split("_")
    request_type = parts[0].upper()
    path = "/".join(parts[1:])
    return request_type, "/"+path

def execute_requests(request_list,host):
    # Call requests agains the endpoint
    responses = []
    for request in request_list:
        logger.debug(f"Debugging: Request is {request}")
        func = request.function
        if not func:
            print("Failed to get function from request: ", request)
            return Result.ERROR,None
        if not func.arguments:
            print("Failed to get arguments from function: ", func)
            return Result.ERROR,None
        args = json.loads(func.arguments)
        func_name = func.name
        logger.debug("Func name is ", func_name)
        request_type, path = func_name_to_path(func_name)
        logger.debug(request_type," ",path)
        logger.debug("Debugging: Request type is ", request_type," with arguments ", args)

        # make request 
        if request_type == "POST":
            try:
                print("Debugging: Making a GET request to ", host+path, "with arguments ", args)
                response = requests.post(host+path, params=args)
                responses.append(response.json())
            except Exception as e:
                print("Failed to make request to ", host+path," cause: ", e)
                return Result.ERROR,None

        if len(responses) != len(request_list):
            return Result.ERROR,None
        return Result.OK, responses


# Main is the cli entrypoint
@click.command()
@click.option('--idl',
        prompt="The file location of the OpenAI IDL json",
        help="If you don't have a OpenAI IDL json then please install the s2o rust crate and convert your swagger.",
        type=click.Path(exists=True))
def main(idl):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    if not client:
        print("Failed to create client")
        sys.exit(1)
    host = os.environ.get("HOST")
    if not host:
        print("Failed to get host")
        sys.exit(1)
    assistant_instructions = os.environ.get("ASSISTANT_INSTRUCTIONS")
    if not assistant_instructions:
        print("Failed to get assistant instructions")
        sys.exit(1)

    with open(idl) as f:
        function_json = json.load(f)

    print("Welcome to the OpenAI API Wrapper")
    print("Type your question and press enter to get started")
    print("Type exit to exit")
    while True:
        prompt = input("> ")
        if prompt == "exit":
            break
        if prompt:
            task = prompt.strip()
            assistant_id, thread_id = setup_assistant(client, task,assistant_instructions,function_json)
            logger.debug(f"Debugging: Useful for checking the generated agent in the playground. https://platform.openai.com/playground?mode=assistant&assistant={assistant_id}")
            logger.debug(f"Debugging: Useful for checking logs. https://platform.openai.com/playground?thread={thread_id}")
            startTime = time.time()
            status,request_list,run_status,run_id = run_assistant(client, assistant_id, thread_id)
            logger.debug(request_list)
            
            
            if status == Result.ERROR:
                logger.debug("Error with running the assistant: ",run_status)
                sys.exit(1)
            
            elif status == Result.PROMPT:
                logger.debug("Debugging: Run completed successfully")
                print(request_list.data[0].content[0].text.value)
                continue
            
            elif status == Result.OK:
                logger.debug(f"Debugging: Total time taken: {time.time() - startTime}")
                result, response = execute_requests(request_list,host)
                if result == Result.OK:
                    print("Responses are: ")
                    for r in response:
                        print(r)
                    continue
                else:
                    print("Found no matching requests")
                    continue