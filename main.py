from fastapi import FastAPI
from pydantic import BaseModel
from bedrock_handler import call_bedrock

app = FastAPI()

class Prompt(BaseModel):
   text: str

@app.post("/chat")
async def chat(prompt: Prompt):
   response = call_bedrock(prompt.text)
   return {"response": response}