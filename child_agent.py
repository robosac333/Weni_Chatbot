import boto3
import requests
import json
import os
from bedrock_handler import call_titan
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENWEATHERMAP_API_KEY")

def get_data(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        output = f"Temperature: {temp} C, Weather: {description}"
        return output
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    except (KeyError, IndexError):
        return "Error: Unable to extract weather data from API response"
    except Exception as e:
        return f"Error: {e}"

user_query = "How is the humidity in Saulo Paulo Like?"
city_name = "Sao Paulo"
data = get_data(city_name)
response = call_titan(data)
print(response)