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
async def titan_child_agent(user_query: str = Query(..., description="User's weather query"), api_docs_url: str = Query(..., description="API docs URL"), api_key: str = Query(..., description="API key")):
    try:
        # Step 1: Fetch API docs
        api_docs = fetch_api_docs(api_docs_url)
        
        if api_docs is None:
            return {"error": "Failed to fetch API docs"}
        # Had to debug the API docs to remove the dataLayer code tracking code
        # It was causing errors to generate the code
        api_docs = api_docs.replace('dataLayer', '').strip()
        
        # Step 2: Generate prompt
        prompt = f"""
        Generate a Python script based on the following API documentation:
        API Documentation:
        {api_docs}
        
        User Query:
        {user_query}

        Requirements:
        1. Create a get_data() function that:
           - Extracts relevant API endpoint and parameters from the documentation
           - Uses the API key: {api_key}
           - Returns data in a standardized format
           - Handles errors gracefully with clear error messages
           - Uses only ASCII characters in responses
        
        2. Use this structure:
            import requests
            import json
            import os
            from bedrock_handler import call_titan
            from dotenv import load_dotenv

            load_dotenv()

            def get_data():
                # Your implementation here
                # Must handle the API call based on the user query
                # Return standardized response format
            
            # Get data and generate response
            data = get_data()
            response = call_titan(data)
            print(response)

        3. The script must:
           - Run automatically without user input
           - Extract all needed parameters from the user query
           - Use proper error handling
           - Return data in a consistent format
           - Use only ASCII characters
        
        Generate only the complete, executable Python code with minimal comments.
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