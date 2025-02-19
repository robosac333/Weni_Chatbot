import boto3
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENWEATHERMAP_API_KEY")
bedrock_client = boto3.client('bedrock-runtime')

def call_titan(prompt: str):
    payload = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 200,
            "stopSequences": [],
            "temperature": 0.5,
            "topP": 0.6
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

def get_weather(city_name: str):
    api_endpoint = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": os.getenv("OPENWEATHERMAP_API_KEY"),
        "units": "metric"
    }

    try:
        response = requests.get(api_endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        return f"Temperature: {int(temperature)} C, Weather: {weather_description}"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

user_query = "How is the weather in Delhi Like?"
city_name = "Delhi"
weather_data = get_weather(city_name)
response = call_titan(f"User Query: {user_query}\nWeather Data: {weather_data}")
print(response)