import requests

# input_query = input("Enter your query: ").strip()
# api_docs_url = input("Enter the API docs URL: ").strip()
# api_key = input("If the API has a key, enter it here if not leave blank: ").strip()

input_query = "Create an AI agent that knows everything about given API documentation"
# api_docs_url = "https://openweathermap.org/api"
# api_key = "3c13f2d6e8beb2b1f742324dbbd8b212"

# api_docs_url = "https://api.nasa.gov/"
# api_key = "ISxBTHQjvQaazVnIHy6322mahQx6fIm9YHzcFuMB"


api_docs_url = "https://newsapi.org/docs/client-libraries/python"
api_key = "17a8051fc49f4cae89ca006f5e4189c6"
base_url = "http://localhost:8000"

params={"user_query": input_query, "api_docs_url": api_docs_url, "api_key": api_key}

# This request generates the child agent
response = requests.get(f"{base_url}/titan_child_agent", params=params)

print("Check the child_agent.py file for the generated code")
print("Agent Response:", response.json())

agent_file = "child_agent.py"

# This request verifies the child agent is valid or not
# response = requests.post(f"http://localhost:8000/verify_agent?agent_file={agent_file}")

print("-----------------------------------------------------------------")
print("Agent Verification Response:")
# print(response.json())