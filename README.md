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
```
    Configure the AWS credentials in the ~/.aws/credentials file.

    To save time and effort in configuring the policies I have given administrator access to the user I am using.

    Also ensure that you have access to the following Bedrock models:
    - Anthropic Claude 3 Sonnet

5. Run the app:

Open a terminal and run the following command to connect to the app:
```
uvicorn main:app --reload
```
    This starts the FastAPI server on http://127.0.0.1:8000

6. Test the app:

Open the test_requests.ipynb file and run the cells to test the app.

Alternatively, you may use postman to test the app by sending a POST request to http://localhost:8000/chat with the following body:
```
{
    "text": "Say hi in one word"
}
```



