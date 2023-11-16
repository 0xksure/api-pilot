from openai import OpenAI
import os 
import time
import sys
import json
import requests
import subprocess
from enum import Enum
import logging

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)


def setup_assistant(client, task):
    # Load function json from file 
    with open("idls/openai/openai.json") as f:
        function_json = json.load(f)
    logger.debug("Debugging: Function json is ", function_json)
    # create a new agent
    assistant = client.beta.assistants.create(
        instructions="You are a wrapper around a payments api. Use the provided endpoints to answer user questions. Sometimes functions has to be combined to achieve the intended result.",
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

class Result(Enum):
    OK = 1
    ERROR = 2
    PROMPT = 3


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
    for request in request_list:
        logger.debug(f"Debugging: Request is {request}")
        
        func = request.function
        args = json.loads(func.arguments)
        func_name = func.name
        logger.debug("Func name is ", func_name)
        request_type, path = func_name_to_path(func_name)
        logger.debug(request_type," ",path)
        logger.debug("Debugging: Request type is ", request_type," with arguments ", args)

        # make request 
        if request_type == "GET":
            try:
                print("Debugging: Making a GET request to ", host+path, "with arguments ", args)
                response = requests.post(host+path, params=args)
                return Result.OK,response.json()
            except Exception as e:
                print("Failed to make request to ", host+path," cause: ", e)
                return Result.ERROR,None

            

if __name__ == "__main__":
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        host = "http://localhost:8000"
        print("Welcome to the OpenAI Payments API Wrapper")
        print("Type your question and press enter to get started")
        while True:
            prompt = input("> ")
            if prompt == '' and p.poll() is not None:
                break
            if prompt:
                task = prompt.strip()
              
            
                assistant_id, thread_id = setup_assistant(client, task)
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
                        if response["balance"]:
                            print("Balance is: ", response["balance"])
                            run = client.beta.threads.runs.submit_tool_outputs(
                                    thread_id=thread_id,
                                    run_id=run_id,
                                    tool_outputs=[
                                        {
                                            "tool_call_id": request_list[0].id,
                                            "output": response["balance"],
                                        },
                                    ]
                                )
                        else:
                            print("Balance was not found. Please try again")
                        continue

       

        

   




