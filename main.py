from fastapi import FastAPI, Query
from pydantic import BaseModel
from bedrock_handler import call_claude, call_titan
from utilities import fetch_api_docs
import requests
import os
import importlib
from io import StringIO
import sys

app = FastAPI()

class Prompt(BaseModel):
   text: str

class UserQuery(BaseModel):
    user_query: str

@app.post("/chat_claude")
async def claude_test(prompt: Prompt):
   response = call_claude(prompt.text)
   return {"response": response}

@app.post("/chat_titan")
async def titan_test(prompt: Prompt):
   response = call_titan(prompt.text)
   return {"response": response}

@app.get("/weather")
async def get_weather():
    try:
        api_docs_url = "https://openweathermap.org/current"
        api_docs = fetch_api_docs(api_docs_url)
        return {"response": api_docs}
    except Exception as e:
        return {"error": str(e)}

@app.post("/user_query")
async def get_user_query(user_query: UserQuery):
    try:
        user_query = user_query.user_query
        return {"response": user_query}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/claude_child_agent")
async def claude_child_agent(user_query: str = Query(..., description="User's weather query")):
        try:
            # Step 1: Fetch API docs
            api_docs_url = "https://openweathermap.org/current"
            api_docs = fetch_api_docs(api_docs_url)

            #Step 3: Generate child agent
            prompt = """
            Generate a Python script based on the following API documentation:
            API Documentation:
            {api_docs}
            
            User Query:
            {user_query}
            The script must:
            1. Use the current weather data endpoint from the API docs above
            2. Have only two core functions:
            - call_claude(): to process user queries
            - get_weather(): to fetch weather data
            3. Use provided API documentation using plain ASCII strings only
            4. All output strings must:
            - Use only characters a-z, A-Z, 0-9, and basic punctuation
            - Format numbers using standard digits
            - No Unicode, emojis, or extended ASCII
            - Weather outputs as 'Temperature: X C, Weather: description'
            5. Use this exact code structure for the Bedrock call:
            
            import boto3
            import requests
            import json
            import os
            from dotenv import load_dotenv

            load_dotenv()
            api_key = os.getenv("OPENWEATHERMAP_API_KEY")
            def call_claude(prompt: str):
                bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
                payload = {{
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "messages": [
                        {{
                            "role": "user",
                            "content": prompt
                        }}
                    ]
                }}

                response = bedrock_client.invoke_model(
                    body=json.dumps(payload),
                    modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                    contentType="application/json",
                    accept="application/json"
                )
                
                response_body = json.loads(response['body'].read())
                return response_body['content'][0]['text']

            4. The get_weather() function must:
            - Extract the API endpoint and parameters from the API docs above
            - Take a city name as input
            - Use os.getenv("OPENWEATHER_API_KEY") for the API key
            - Return temperature in Celsius and weather description
            - Handle errors gracefully
            
            5. The main section should:
            - Use the user query to formulate the get_weather() function call
            - Call get_weather() with the required details from the user query to be able to fetch the weather data
            - Give this weather data to the agent and generate a natural language response
            
            Generate only the complete, executable Python code with no explanations or comments.
            NOTE: The generated code should not ask any user input and should be able to fetch the weather data based on the user query.
            IMPORTANT: Use only ASCII characters in all string outputs. 
            Do not use special characters like degree symbols (°) or other Unicode characters. Use 'C' for Celsius.
            """.format(api_docs=api_docs, user_query=user_query)

            response = call_claude(prompt)

            # Step 3: Save to a file
            with open("child_agent.py", "w") as file:
                file.write(response)

            return {"message": "Child agent successfully created", "response": response}

        except Exception as e:
            return {"error": str(e)}
        
@app.get("/titan_child_agent")
async def titan_child_agent(user_query: str = Query(..., description="User's weather query")):
    try:
        # Step 1: Fetch API docs
        api_docs_url = "https://openweathermap.org/current"
        api_docs = fetch_api_docs(api_docs_url)
        
        # Had to debug the API docs to remove the dataLayer code tracking code
        # It was causing errors to generate the code
        api_docs = api_docs.replace('dataLayer', '').strip()
        
        # Step 2: Generate prompt
        prompt = f"""
        Generate a Python script based on the following API documentation:
        API Documentation:
        Current weather data API endpoint: api.openweathermap.org/data/2.5/weather?q={{city name}}&appid={{API key}}

        User Query:
        {user_query}

        The script must:
        1. Use the current weather data endpoint from the API docs above
        2. Have only two core functions:
        - call_titan(): to process user queries
        - get_weather(): to fetch weather data
        3. Use provided API documentation using plain ASCII strings only
        4. All output strings must:
        - Use only characters a-z, A-Z, 0-9, and basic punctuation
        - Format numbers using standard digits
        - No Unicode, emojis, or extended ASCII
        - Weather outputs as 'Temperature: X C, Weather: description'

        5. Use this exact code structure for the Bedrock call:

        import boto3
        import requests
        import json
        import os
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        bedrock_client = boto3.client('bedrock-runtime')

        def call_titan(prompt: str):
            payload = {{
                "inputText": prompt,
                "textGenerationConfig": {{
                    "maxTokenCount": 200,
                    "stopSequences": [],
                    "temperature": 0.5,
                    "topP": 0.6
                }}
            }}

            response = bedrock_client.invoke_model(
                body=json.dumps(payload),
                modelId="amazon.titan-text-express-v1",
                contentType="application/json",
                accept="application/json"
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['results'][0]['outputText']

        6. The get_weather() function must:
        - Extract the API endpoint and parameters from the API docs above
        - Take a city name as input
        - Use os.getenv("OPENWEATHER_API_KEY") for the API key
        - Return temperature in Celsius and weather description
        - Handle errors gracefully

        7. The main section should:
        - Use the user query to formulate the get_weather() function call
        - Call get_weather() with the required details from the user query to be able to fetch the weather data
        - Give this weather data to the agent and generate a natural language response

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