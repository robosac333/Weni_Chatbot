import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")

def call_claude(prompt: str):
    """
    For sending a request to AWS Bedrock to generate a response from Claude.
    """
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2500,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = bedrock_client.invoke_model(
        body=json.dumps(payload),
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        contentType="application/json",
        accept="application/json"
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['content'][0]['text']

def call_titan(prompt: str):
    """
    For sending a request to AWS Bedrock to generate a response from Titan Express.
    """
    payload = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 200,
            "stopSequences": [],
            "temperature": 0.3,
            "topP": 0.4
        }
    }

    response = bedrock_client.invoke_model(
        body=json.dumps(payload),
        modelId="amazon.titan-text-express-v1",
        contentType="application/json",
        accept="application/json"
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['results'][0]['outputText']

if __name__ == "__main__":
    print(call_titan("Say hi in one word"))
