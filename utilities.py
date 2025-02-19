import requests
def fetch_api_docs(api_docs_url):
    """Fetch API documentation from the given URL."""
    try:
        response = requests.get(api_docs_url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Error fetching API docs: {str(e)}"
