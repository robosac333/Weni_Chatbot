from fastapi import FastAPI, Query
from pydantic import BaseModel
from bedrock_handler import call_claude, call_titan
from utilities import fetch_api_docs, extract_python_code
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
        {user_query}, 
        {api_docs}
        Parse API documentation and generate Python code that:

        1. EXTRACTION (from provided API documentation):
            - Extract the Base URL and endpoint paths correctly
            - Required/optional parameters
            - Authentication requirements
            - Response format
            - Error codes

        2.  Use this exact code structure for the Bedrock call:
            ```python
            import requests
            import json
            from bedrock_handler import call_titan
            
            api_key = {api_key}  # Include only if required by API
            ```
    
                
        3. REQUIREMENTS:
        - Use exact endpoints/parameters from documentation
            - Implement authentication as specified
            - Implement all the features mentioned in the API documentation
            - Handle errors according to documentation
            - Use only ASCII characters
            - Use only characters a-z, A-Z, 0-9, and basic punctuation
            - No Unicode, symbols such as degree etc, emojis, or extended ASCII

        4. OUTPUT:
            - Make it like a chatbot (AI agent), that can answer questions that are related to the given API.
            - If asked any question that is not related to the API, just say "Sorry, the question above is irrelevant" and explain what this AI is built for 
            - Once the chatbot is started, provide accurate instructions on how to input the query based on the code you write.
            - if user query is not relevant, generate human-like response using the call_titan function that is already implemented, you can input prompt to get a response - call_titan(prompt)            

                        

        Generate code following everything given in above structure and based on provided API documentation.
        IMPORTANT: Output only the clean executable code and nothing other than the code,
        so that if the output from the llm is written to a python file, the file is valid and executable.
        """

        # Step 3: Calling mother agent to generate the child agent
        response = call_claude(prompt)


        if "python" in response:
            response = extract_python_code(response)
        
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