import boto3
import requests
import json
import os
from bedrock_handler import call_titan
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")

def get_data():
    lat = 37.7749
    lon = -122.4194
    
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        print(data)
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        
        weather_data = f"Temperature: {temp} C, Weather: {description}"
        return weather_data
    
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

data = get_data()

# response = call_titan(data)
# print(response)