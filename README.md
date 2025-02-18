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
4. Run the script
