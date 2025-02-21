import requests
import json
from bedrock_handler import call_titan

# News API key (required for authentication)
api_key = "17a8051fc49f4cae89ca006f5e4189c6"

# Base URL
base_url = "https://newsapi.org/v2/"

def get_top_headlines(q=None, sources=None, category=None, language='en', country='us'):
    """
    Get current top headlines.
    
    Parameters:
    q (str, optional): Keywords or a phrase to search for.
    sources (str, optional): A comma-seperated string of identifiers for the news sources or blogs you would like headlines from.
    category (str, optional): The category you would like to get headlines for.
    language (str, default 'en'): The language you want to get headlines for.
    country (str, default 'us'): The country you want to get headlines for.
    
    Returns:
    dict: Response from the API (JSON format)
    """
    endpoint = "top-headlines"
    params = {
        'q': q,
        'sources': sources,
        'category': category,
        'language': language,
        'country': country,
        'apiKey': api_key
    }
    response = requests.get(base_url + endpoint, params=params)
    return response.json()

def get_everything(q, sources=None, domains=None, from_param=None, to=None, language='en', sort_by='relevancy', page=1):
    """
    Search through millions of articles from over 80,000 large and small news sources and blogs.
    
    Parameters:
    q (str): Keywords or a phrase to search for.
    sources (str, optional): A comma-seperated string of identifiers for the news sources or blogs you would like headlines from.
    domains (str, optional): A comma-seperated string of domains (e.g. bbc.co.uk, techcrunch.com) to restrict the search to.
    from_param (str, optional): A date and optional time for the oldest article allowed (e.g. 2018-01-01 or 2018-01-01T10:20:00)
    to (str, optional): A date and optional time for the newest article allowed.
    language (str, default 'en'): The language you want to get headlines for.
    sort_by (str, default 'relevancy'): The order to sort the articles in.
    page (int, default 1): Use this to page through the results.
    
    Returns:
    dict: Response from the API (JSON format)
    """
    endpoint = "everything"
    params = {
        'q': q,
        'sources': sources,
        'domains': domains,
        'from': from_param,
        'to': to,
        'language': language,
        'sortBy': sort_by,
        'page': page,
        'apiKey': api_key
    }
    response = requests.get(base_url + endpoint, params=params)
    return response.json()

def get_sources(category=None, language='en', country='us'):
    """
    Get a list of news sources.
    
    Parameters:
    category (str, optional): The category you would like to get sources for.
    language (str, default 'en'): The language you want to get sources for.
    country (str, default 'us'): The country you want to get sources for.
    
    Returns:
    dict: Response from the API (JSON format)
    """
    endpoint = "top-headlines/sources"
    params = {
        'category': category,
        'language': language,
        'country': country,
        'apiKey': api_key
    }
    response = requests.get(base_url + endpoint, params=params)
    return response.json()

def start():
    print("Welcome to the News API chatbot!")
    print("You can ask me questions related to current weather news and trends. To get started, enter a query like:")
    print("'What are the top headlines for technology?'")
    print("'Find articles about bitcoin'")
    print("'List sources for business news'")
    
    while True:
        query = input("> ")
        if "top headlines" in query.lower():
            try:
                q = None
                sources = None
                category = None
                params = query.lower().split()
                for param in params:
                    if param == "for":
                        category = params[params.index(param)+1]
                    elif param == "from":
                        sources = params[params.index(param)+1]
                    elif param == "about":
                        q = params[params.index(param)+1]
                
                response = get_top_headlines(q, sources, category)
                print(json.dumps(response, indent=2))
            except Exception as e:
                print(f"Error: {e}")
        
        elif "articles about" in query.lower():
            try:
                q = query.split("about")[-1].strip()
                response = get_everything(q)
                print(json.dumps(response, indent=2))
            except Exception as e:
                print(f"Error: {e}")
        
        elif "sources for" in query.lower():
            try:
                category = query.split("for")[-1].strip()
                response = get_sources(category=category)
                print(json.dumps(response, indent=2))
            except Exception as e:
                print(f"Error: {e}")
        
        else:
            prompt = "Sorry, the question above is irrelevant. This AI is built to help you find news articles and sources using the News API. " + query
            print(call_titan(prompt))

if __name__ == "__main__":
    start()