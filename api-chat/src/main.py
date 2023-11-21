from flask import Flask
from flask import request,make_response,abort
import json
import logging
from api_assistant import main,s2opy


logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

app = Flask(__name__)

@app.route("/ask",methods=["POST"])
def ask():  
    if request.method == "POST":
        response = make_response()
        config = main.utils.get_config()
        data = request.get_json()
        print("Data is ", data)
        swagger_file = data["swagger_file"]
        if not swagger_file:
            abort(400,"Error: No swagger file provided")
        query = data["query"]
        if not query:
          abort(400,"Error: No Query provided")
        
        function_json = json.loads(s2opy.swagger_from_file(swagger_file))
        assistant = main.OpenAIAssistant.setup_assistant(config["api_key"],config["assistant_instructions"],function_json,logger)
        result = assistant.run_assistant(query)
            
        if result.is_err():
            message = result.err()
            print(message)

            return {
                "message": message
            }   
        else:
            request_list = result.unwrap()
            print("Sending requests: ", request_list)
            return {
                "message": "Success",
                "requests": request_list
            }

    else: 
        abort(400,"Error: Only POST requests are supported")
        