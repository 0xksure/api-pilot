from common.interface import AssistantInterface
from common.request import Request,Requests
from openai import OpenAI
import time
import logging
import json
from common.interface import Result,func_name_to_path
from result import Err,Ok,Result

class OpenAIAssistant(AssistantInterface):

    """
        init initializes the assistant and a thread.

        Args:
            client: The OpenAI client
            task: The task to be performed by the assistant
            assistant_instructions<str>: The instructions for the assistant
            function_json<dict>: The json representation of the functions

        Returns:
            assistant_id<str>, thread_id<str>: The assistant id and thread id
    """
    def __init__(self, client,assistant_id: str, thread_id: str,logger: logging.Logger):
        super().__init__(client,assistant_id, thread_id,logger)

   
    def setup_assistant(key, assistant_instructions,function_json,logger):
        client = OpenAI(api_key=key)
        
        # Load function json from file 
        logger.debug("Debugging: Function json is ", function_json)
        # create a new agent
        assistant = client.beta.assistants.create(
            instructions=assistant_instructions,
            model="gpt-3.5-turbo",
            tools=function_json
        )

        # Create a new thread
        thread = client.beta.threads.create()


        # Return the assistant ID and thread ID
        return OpenAIAssistant(client,assistant.id, thread.id,logger)


    def __convert_tool_call_to_request(self,tool_call)-> Result[Request,str] :   
        func = tool_call.function
        if not func:
            print("Failed to get function from tool_call: ", tool_call)
            return Err("failed to get function from tool_call")
        
        arguments = json.loads(func.arguments)
        func_name = func.name
        request_type,path = func_name_to_path(func_name)

        return Ok(Request(request_type,path,arguments))

    def __convert_openai_required_actions_to_requests(self,required_actions)-> Result[Requests,str]:
        tool_calls = required_actions.submit_tool_outputs.tool_calls
        requests = Requests()
        for tool_call in tool_calls:
            result = self.__convert_tool_call_to_request(tool_call)
            if result.is_err():
                return Err(result.err())
            requests.append(result.unwrap())
        return Ok(requests)
       

    """
        run_assistant takes the assistant and thread id and runs the assistant.

        It loops until the run status is either "completed" or "requires_action".
        require_action means that the assistant has found a function that can be called.
        completed means that the assistant is finished and most likely does not have an action.

        Args: 
            client: The OpenAI client
            assistant_id<str>: The assistant id
            thread_id<str>: The thread id
        Returns: 
            Result: The result of the run
            request_list: A list of requests that can be called
            run_status: The status of the run
            run_id: The id of the run
    """
    def run_assistant(self, task) -> Result[Requests,str]:

        # Create a new thread message with the provided task
        self.client.beta.threads.messages.create(
            self.thread_id,
            role="user",
            content=task,
            )

        # Create a new run for the given thread and assistant
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.id
        )

        # Loop until the run status is either "completed" or "requires_action"
        while run.status == "in_progress" or run.status == "queued":
            time.sleep(0.2)
            self.logger.debug("Debugging: Run status is ", run.status)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=run.id
            )

            # At this point, the status is either "completed" or "requires_action"
            if run.status == "completed":
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread_id
                ).data[0].content[0].text.value
                return Err(messages)
            
            if run.status == "requires_action":
                self.logger.debug("Debugging: The run requires an action")
                self.logger.debug("Required actions: ",run.required_action)
                self.logger.info("Output: ", run.required_action.submit_tool_outputs.tool_calls)
                request_results = self.__convert_openai_required_actions_to_requests(run.required_action)
                if request_results.is_err():
                    return Err(request_results.err())
                return Ok(request_results.unwrap())

        return Err("failed with undefined run status")
        