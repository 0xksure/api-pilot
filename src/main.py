from openai import OpenAI
import os 
import time
import sys
import json
import requests
import subprocess
from enum import Enum
import logging

def setup_assistant(client, task):
    # Load function json from file 
    with open("idls/openai/openai.json") as f:
        function_json = json.load(f)
    logging.debug("Debugging: Function json is ", function_json)
    # create a new agent
    assistant = client.beta.assistants.create(
    instructions="You are a wrapper around a payments api. Use the provided endpoints to answer user questions. Sometimes functions has to be combined to achieve the intended result.",
    model="gpt-4-1106-preview",
    tools=[function_json[0]]
    )


    # Create a new thread
    thread = client.beta.threads.create()

    # Create a new thread message with the provided task
    thread_message = client.beta.threads.messages.create(
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
        logging.debug("Debugging: Run status is ", run.status)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

        # At this point, the status is either "completed" or "requires_action"
        if run.status == "completed":
            return (Result.PROMPT,client.beta.threads.messages.list(
              thread_id=thread_id
            ),run.status)
        
        if run.status == "requires_action":
            logging.debug("Debugging: The run requires an action")
            logging.debug("Required actions: ",run.required_action)
            #args = json.loads(run.required_action.submit_tool_outputs.tool_calls[0])
            logging.debug("Output: ", run.required_action.submit_tool_outputs.tool_calls)
            # run = client.beta.threads.runs.submit_tool_outputs(
            #     thread_id=thread_id,
            #     run_id=run.id,
            #     tool_outputs=[
            #         {
            #             "tool_call_id": run.required_action.submit_tool_outputs.tool_calls[0].id,
            #             "output": run.required_action.submit_tool_outputs.tool_calls[0],
            #         },
            #     ]
            # )
            return  (Result.OK ,run.required_action.submit_tool_outputs.tool_calls,run.status)

    return (Result.ERROR, None,run.status)
            

def func_name_to_path(func_name: str):
    parts = func_name.split("_")
    request_type = parts[0].upper()
    path = "/".join(parts[1:])
    return request_type, "/"+path

def execute_requests(request_list):
    # Call requests agains the endpoint
    for request in request_list:
        logging.debug(f"Debugging: Request is {request}")
        
        func = request.function
        args = json.loads(func.arguments)
        func_name = func.name
        logging.debug("Func name is ", func_name)
        request_type, path = func_name_to_path(func_name)
        logging.debug(request_type," ",path)
        logging.debug("Debugging: Request type is ", request_type," with arguments ", args)

        # make request 
        if request_type == "GET":
            try:
                logging.debug("Debugging: Making a GET request to ", host+path, "with arguments ", args)
                response = requests.get(host+path, params=args)
                logging.debug("Debugging: Response is ", response.json(), " with status code ", response.status_code)
            except:
                print("Failed to make request to ", host+path)

            

if __name__ == "__main__":
        print("Welcome to the OpenAI Payments API Wrapper")
        print("Type your question and press enter to get started")
        while True:
            prompt = input("> ")
            if prompt == '' and p.poll() is not None:
                break
            if prompt:
                task = prompt.strip()
                client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
                host = "http://localhost:8080"
            
                assistant_id, thread_id = setup_assistant(client, task)
                logging.debug(f"Debugging: Useful for checking the generated agent in the playground. https://platform.openai.com/playground?mode=assistant&assistant={assistant_id}")
                logging.debug(f"Debugging: Useful for checking logs. https://platform.openai.com/playground?thread={thread_id}")
                startTime = time.time()
                status,request_list,run_status = run_assistant(client, assistant_id, thread_id)
                logging.debug(request_list)
                
                
                if status == Result.ERROR:
                    logging.debug("Error with running the assistant: ",run_status)
                    sys.exit(1)
                
                elif status == Result.PROMPT:
                    logging.debug("Debugging: Run completed successfully")
                    print(request_list.data[0].content[0].text.value)
                    continue
                
                elif status == Result.OK:
                    logging.debug(f"Debugging: Total time taken: {time.time() - startTime}")
                    execute_requests(request_list)
       

        

   




