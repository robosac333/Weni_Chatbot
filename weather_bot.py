import requests
import json
from bedrock_handler import call_titan

api_key = "3c13f2d6e8beb2b1f742324dbbd8b212"  # Include only if required by API

base_url = "https://api.openweathermap.org/"

def get_current_weather(city_name):
    endpoint = "data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url + endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        return f"The current weather in {city_name} is {description} with a temperature of {temperature}C."
    else:
        return f"Error: {response.status_code} - {response.text}"

def get_forecast(city_name):
    endpoint = "data/2.5/forecast"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url + endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        forecast_list = data["list"]
        forecast_text = "Here is the forecast for the next few days in {city_name}:\n\n".format(city_name=city_name)
        for forecast in forecast_list[:5]:  # Show only the first 5 forecasts
            forecast_date = forecast["dt_txt"]
            description = forecast["weather"][0]["description"]
            temperature = forecast["main"]["temp"]
            forecast_text += f"{forecast_date}: {description}, {temperature}C\n"
        return forecast_text
    else:
        return f"Error: {response.status_code} - {response.text}"

def start_chatbot():
    print("Welcome to the OpenWeatherMap API chatbot!")
    print("You can ask me about current weather conditions or forecasts for a specific city.")
    print("To get the current weather, say 'current weather in [city]'.")
    print("To get the forecast, say 'forecast for [city]'.")

    while True:
        user_input = input("> ").lower()
        if "current weather in" in user_input:
            city_name = user_input.replace("current weather in", "").strip()
            response = get_current_weather(city_name)
            print(response)
        elif "forecast for" in user_input:
            city_name = user_input.replace("forecast for", "").strip()
            response = get_forecast(city_name)
            print(response)
        else:
            prompt = "Sorry, the question above is irrelevant. This chatbot is built to provide current weather conditions and forecasts for cities using the OpenWeatherMap API. " + user_input
            response = call_titan(prompt)
            print(response)

start_chatbot()