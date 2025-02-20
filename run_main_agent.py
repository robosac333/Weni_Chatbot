import requests

input_query = input("Enter your query: ").strip()
api_docs_url = input("Enter the API docs URL: ").strip()
api_key = input("If the API has a key, enter it here if not leave blank: ").strip()
base_url = "http://localhost:8000"

params={"user_query": input_query, "api_docs_url": api_docs_url, "api_key": api_key}

# This request generates the child agent
response = requests.get(f"{base_url}/titan_child_agent", params=params)

print("Check the child_agent.py file for the generated code")
print("Agent Response:", response.json())

agent_file = "child_agent.py"

# This request verifies the child agent is valid or not
response = requests.post(f"http://localhost:8000/verify_agent?agent_file={agent_file}")

print(response.json())