# Weni_Chatbot
Created an AI Agent using AWS Bedrock, capable of automatically creating other agents from an API documentation.

## Steps
1. Create a conda environment
```
conda create -n weni python=3.10
```

2. Install the required packages
```
pip install -r requirements.txt
```

3. Create a .env file and add the following variables:
```
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_REGION=your_region
OPENWEATHERMAP_API_KEY=3c13f2d6e8beb2b1f742324dbbd8b212
```
    To save time and effort in configuring the policies I have given administrator access to the user I am using and I suggest you to do the same.

    Also ensure that you have access to the following Bedrock models:
    - Anthropic Claude 3 Sonnet
    - Titan Text G1 - Express

5. Run the app:

Open a terminal and run the following command to connect to the app:
```
uvicorn main:app --reload
```
    This starts the FastAPI server on http://127.0.0.1:8000

6. Test the app:

Open the test_requests.ipynb file and run the cells to test the app and configure the setup such as connection to the API and the LLMs.

I have configured the Claude 3 Sonnet and Titan Text Express models to be used as the mother and the child agents respectively.

Alternatively, you may use postman to test the app by sending a POST request to http://localhost:8000/chat with the following body:
```
{
    "text": "Say hi in one word"
}
```

## Recieve response from a Weathermap API

I have used the OpenWeatherMap API to get the currentweather data for a city with all the attributes mainly because it is free.

The Link to the API Docs is: https://openweathermap.org/current

In addition, it has other API Docs which can be accessed by the child agent to get the 

To get the API key, you need to sign up on the OpenWeatherMap website and get the API key.

To make the work easier, I have added the API key to the .env file and specified the key here if you don't want to configure the api key yourself.
```
OPENWEATHERMAP_API_KEY=3c13f2d6e8beb2b1f742324dbbd8b212
```



