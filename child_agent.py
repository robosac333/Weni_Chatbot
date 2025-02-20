import boto3
import requests
import json
import os
from bedrock_handler import call_titan
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENWEATHERMAP_API_KEY")

def get_data():
    latitude = 37.7749
    longitude = -122.4194
    api_url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        
        result = f"Temperature: {temperature} C, Weather: {weather_description}"
        return result
    
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

data = get_data()
response = call_titan(data)
print(response)