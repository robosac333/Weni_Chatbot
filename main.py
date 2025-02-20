from fastapi import FastAPI, Query
from pydantic import BaseModel
from bedrock_handler import call_claude, call_titan
from utilities import fetch_api_docs
import requests
import os
import importlib
from io import StringIO
import sys
from utilities import test_apis

app = FastAPI()

class Prompt(BaseModel):
   text: str

@app.post("/chat_claude")
async def claude_test(prompt: Prompt):
   response = call_claude(prompt.text)
   return {"response": response}

@app.post("/chat_titan")        
async def titan_test(prompt: Prompt):
   response = call_titan(prompt.text)
   return {"response": response}

@app.get("/weather")
async def get_weather(api_docs_url: str = Query(..., description="API docs URL")):
    try:
        api_docs = fetch_api_docs(api_docs_url)
        return {"response": api_docs}
    except Exception as e:
        return {"error": str(e)}

@app.post("/user_query")
async def get_user_query(user_query: str = Query(..., description="User's weather query")):
    try:
        return {"response": user_query}  
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/titan_child_agent")
async def titan_child_agent(user_query: str = Query(..., description="User's weather query"), api_name: str = Query(..., description="API docs URL")):
    try:
        # Step 1: Fetch API docs
        api_docs = fetch_api_docs(test_apis[api_name]['url'])
        
        if api_docs is None:
            return {"error": "Failed to fetch API docs"}
        # Had to debug the API docs to remove the dataLayer code tracking code
        # It was causing errors to generate the code
        api_docs = api_docs.replace('dataLayer', '').strip()
        
        # Step 2: Generate prompt
        prompt = f"""
        Generate a Python script based on the following API documentation:
        API Documentation:
        API endpoint: {api_docs}
        
        User Query:
        {user_query}

        The script must:
        1. Use the current weather data endpoint from the API docs above
        2. Have only one function to write the code for:
        - get_data(): to fetch the relevant data from the API
        3. Use provided API documentation using plain ASCII strings only
        4. All output strings must:
        - Use only characters a-z, A-Z, 0-9, and basic punctuation
        - Format numbers using standard digits
        - No Unicode, emojis, or extended ASCII
        - Weather outputs as 'Temperature: X C, Weather: description'
        5. Do not write the code for the call_titan(prompt) function, just use it as it is from the bedrock_handler.py file
        6. Use this exact code structure for the Bedrock call:
        
            import boto3
            import requests
            import json
            import os
            from bedrock_handler import call_titan
            from dotenv import load_dotenv

            load_dotenv()

            api_key = API key: {test_apis[api_name]["API_KEY"]}

        IMPORTANT: after this write the get_data() function and then call the Titan model
        data = get_data()
        response = call_titan(data)

        6. The get_data() function must:
        - Extract the API endpoint and parameters from the API docs above
        - Take a city name as input
        - Use os.getenv("OPENWEATHER_API_KEY") for the API key
        - Return temperature in Celsius and weather description
        - Handle errors gracefully

        7. The main section should:
        - Use the user query to formulate the get_data() function call
        - Call get_data() with the required details from the user query to be able to fetch the weather data
        - Give this weather data to the agent and generate a natural language response
        - Make sure to print the response from the Titan model

        Generate only the complete, executable Python code with no explanations or comments.
        NOTE: The generated code should not ask any user input and should be able to fetch the weather data based on the user query.
        IMPORTANT: Use only ASCII characters in all string outputs. 
        Do not use special characters like degree symbols (°) or other Unicode characters. Use 'C' for Celsius.
        """

        # Step 3: Calling mother agent to generate the child agent
        response = call_claude(prompt)

        # Step 4: Save to a file
        with open("child_agent.py", "w") as file:
            file.write(response)

        return {"message": "Child agent successfully created", "response": response}

    except Exception as e:
        return {"error": str(e)}
    
@app.post("/verify_agent")
async def verify_agent(agent_file: str = Query(..., description="Path to the agent file")):
    try:
        # Using compile to check if the code is in valid syntax
        with open(agent_file, 'r') as f:
            code = f.read()
            compile(code, agent_file, 'exec')
        
        stdout = StringIO()
        sys.stdout = stdout

        # Executing the code directly using exec() in a new namespace
        namespace = {}
        exec(code, namespace)

        # Configured stdout to print the output
        sys.stdout = sys.__stdout__
        output = stdout.getvalue()

        return {
            "status": "success",
            "syntax_valid": True,
            "message": "Agent file executed successfully",
            "output": output
        }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }