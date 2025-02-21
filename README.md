# Weni_Chatbot
Created an AI Agent using AWS Bedrock, capable of automatically creating other agent chatbot answering questions related to an API Documentation.

## Overview
The current setup uses the Anthropic Claude 3 Sonnet Bedrock agent to generate a Titan Text G1 - Express Bedrock agent creating an interactive chatbot!!

Based on the user query and the input API Documentation, the Claude main agent has been prompt engineered to generate an executable python code with no errors.
It writes the code to a file called child_agent.py which can be executed to generate a chatbot answering questions pertaining to the functionality demanded by the user.

The app has two configurations to run the main agent.

1. Run the app as it is if you are sure if everything is configured correctly.
2. When configuring the app for the first time, run the test_automation.ipynb file to check if:
- The api-doc is retrievable from the API Documentation URL.
- The LLM requests from bedrock are working fine.
- The Claude main agent is able to generate the executable python code with no errors.

## Steps

To set up the app, follow the steps below:

### 1. Create a conda environment
```
conda create -n weni python=3.10
```

### 2. Install the required packages
```
pip install -r requirements.txt
```

### 3. Create a .env file and add the following variables:
```
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_REGION=your_region
```
    To save time and effort in configuring the policies I have given administrator access to the user I am using and I suggest you to do the same.

    Also ensure that you have access to the following Bedrock models:
    - Anthropic Claude 3 Sonnet
    - Titan Text G1 - Express

### 4. Run the app:

Open a terminal and run the following command to connect to the app:
```
uvicorn main:app --reload
```
    This starts the FastAPI server on http://127.0.0.1:8000

### 5. Test the app:

Open the test_requests.ipynb file and run the cells to test the app and configure the setup such as connection to the API and the LLMs.

- If you want to configure your own API doc, configure and check if the api-doc is retrievable from the API Documentation URL with the current retrieval method. Also attach the API key to the dictionary in first cell of the notebook.

- Check all the other configurations are working and the child agent is able to generate the executable python code with no errors.

### 6. Run the main agent directly

To run the main agent directly, run the following command:
```
python run_main_agent.py
```
If you want to directly see already generated child agents, run the .py files in the generated_agents folder such as weather_bot.py, news_bot.py, etc.

### Sample Input 1
```
Enter your query: Create an AI agent that knows everything about given API documentation

Enter the API docs URL: https://api.nasa.gov/

Enter the API key: ISxBTHQjvQaazVnIHy6322mahQx6fIm9YHzcFuMB
```



## Disclaimer
- When running the main agent, some times it generates an error for api calls.The error is as follows:
```
'error': 'An error occurred (ThrottlingException) when calling the InvokeModel operation (reached max retries: 4): Too many requests, please wait before trying again. You have sent too many requests.  Wait before trying again.'
```
This ThrottlingException occurs because AWS Bedrock has rate limits on the number of requests per second, and your application is exceeding the allowed request rate.


- Sometimes the main agent may not be able to generate the child agent perfectly (some errors may occur), Re-run the main agent again which will generate a better child agent. This can be permanently overcome by using a better main agent.


- When running the child_agent.py file, some times it generates api_token errors. In that case, you are requested to run the main agent again and generate the child agent again and the agent will work fine. 

## Demos
Here are the attached Videos of some demos

[Weather Bot](https://drive.google.com/file/d/1Yu8jNRNEfpvj7m5A_dzjgDSSSqgk-3ZY/view?usp=sharing)

[Nasa Bot](https://drive.google.com/file/d/1Nwjg8mC1KH7pNYJ3vQpwCad2PxmLTcq8/view?usp=sharing)

[News Bot](https://drive.google.com/file/d/1uyTnyGmXBf2DYdw0PaWh3YByrTe85y1U/view?usp=sharing)




