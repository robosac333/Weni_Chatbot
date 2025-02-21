import requests
import json
from bedrock_handler import call_titan

API_KEY = '17a8051fc49f4cae89ca006f5e4189c6'
BASE_URL = 'https://newsapi.org/v2'

def get_top_headlines(q=None, sources=None, category=None, language='en', country='us'):
    url = f'{BASE_URL}/top-headlines'
    params = {
        'q': q,
        'sources': sources,
        'category': category,
        'language': language,
        'country': country,
        'apiKey': API_KEY
    }
    params = {k: v for k, v in params.items() if v is not None}
    response = requests.get(url, params=params)
    handle_errors(response)
    return response.json()

def get_everything(q=None, sources=None, domains=None, from_param=None, to=None, language='en', sort_by='relevancy', page=1):
    url = f'{BASE_URL}/everything'
    params = {
        'q': q,
        'sources': sources,
        'domains': domains,
        'from': from_param,
        'to': to,
        'language': language,
        'sortBy': sort_by,
        'page': page,
        'apiKey': API_KEY
    }
    params = {k: v for k, v in params.items() if v is not None}
    response = requests.get(url, params=params)
    handle_errors(response)
    return response.json()

def get_sources(category=None, language='en', country='us'):
    url = f'{BASE_URL}/top-headlines/sources'
    params = {
        'category': category,
        'language': language,
        'country': country,
        'apiKey': API_KEY
    }
    params = {k: v for k, v in params.items() if v is not None}
    response = requests.get(url, params=params)
    handle_errors(response)
    return response.json()

def handle_errors(response):
    if response.status_code == 200:
        return
    elif response.status_code == 401:
        raise Exception('Your API key is invalid or incorrect.')
    elif response.status_code == 429:
        raise Exception('You have exceeded the rate limit.')
    elif response.status_code == 400:
        raise Exception('Bad request.')
    else:
        raise Exception(f'Error: {response.status_code} - {response.text}')

def start_chatbot():
    print('Welcome to the News API chatbot!')
    print('This chatbot can answer questions related to the News API documentation.')
    print('To search for news articles, use the following format:')
    print('get_top_headlines q=<query> sources=<sources> category=<category>')
    print('To get curated breaking news headlines, use:')
    print('get_top_headlines country=<country_code> category=<category>')
    print('To search for all news articles, use:')
    print('get_everything q=<query> sources=<sources> domains=<domains> from=<start_date> to=<end_date>')
    print('To get available news sources, use:')
    print('get_sources category=<category> country=<country_code>')
    print('Type "exit" to quit the chatbot.')

    while True:
        query = input('Enter your query: ').strip().lower()
        if query == 'exit':
            break

        if query.startswith('get_top_headlines'):
            try:
                params = parse_query(query, 'get_top_headlines')
                response = get_top_headlines(**params)
                print(json.dumps(response, indent=2))
            except Exception as e:
                print(f'Error: {e}')

        elif query.startswith('get_everything'):
            try:
                params = parse_query(query, 'get_everything')
                response = get_everything(**params)
                print(json.dumps(response, indent=2))
            except Exception as e:
                print(f'Error: {e}')

        elif query.startswith('get_sources'):
            try:
                params = parse_query(query, 'get_sources')
                response = get_sources(**params)
                print(json.dumps(response, indent=2))
            except Exception as e:
                print(f'Error: {e}')

        else:
            prompt = f"Sorry, the question '{query}' is irrelevant. This AI is built to interact with the News API. Please provide a query in the correct format."
            response = call_titan(prompt)
            print(response)

def parse_query(query, endpoint):
    params = {}
    query_parts = query.split(' ')
    for part in query_parts[1:]:
        key, value = part.split('=')
        params[key] = value
    return params

start_chatbot()