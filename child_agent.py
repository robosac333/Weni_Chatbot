import boto3
import requests
import json
import os
from bedrock_handler import call_titan
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENWEATHERMAP_API_KEY")

def get_data(city):
    api_endpoint = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    try:
        response = requests.get(api_endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        weather_info = f"Temperature: {temperature} C, Weather: {description}"
        return weather_info
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

prompt = f"How is the humidity in Sao Paulo Like?"
response = call_titan(prompt)

city = "Sao Paulo"
weather_data = get_data(city)
result = f"{response}\n\n{weather_data}"
print(result)