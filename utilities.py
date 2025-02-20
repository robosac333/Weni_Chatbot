import requests
import time
from urllib.parse import urljoin

test_apis = {
    # OpenWeather
    "Weather": {"url" : "https://openweathermap.org/api",
    "API_KEY" : "3c13f2d6e8beb2b1f742324dbbd8b212"},
    # 2. Reddit
    "Reddit": {"url" : "https://www.reddit.com/dev/api/",
    "API_KEY" : ""},
    # 3. OpenExchangeRates  
    "Currency": {"url" : "https://docs.openexchangerates.org/reference/api-introduction",
    "API_KEY" : ""},
    # 4. NASA API 
    "NASA": {"url" : "https://api.nasa.gov/",
    "API_KEY" : "ISxBTHQjvQaazVnIHy6322mahQx6fIm9YHzcFuMB"},
    # 5. News-API 
    "News": {"url" : "https://newsapi.org/docs/client-libraries/python",
    "API_KEY" : "17a8051fc49f4cae89ca006f5e4189c6"},
}

def fetch_api_docs(base_url):
    """Fetch API documentation from the given URL."""
    try:
        common_paths = [
            '',
            '/api-docs',
            '/swagger',
            '/swagger-ui',
            '/swagger-ui.html',
            '/swagger/index.html',
            '/api/swagger',
            '/api/docs',
            '/docs/api',
            '/openapi.json',
            '/openapi.yaml',
            '/docs',
            '/redoc',
            '/api-reference',
            '/developer',
            '/developers',
            '/documentation',
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        for path in common_paths:
            try:
                
                url = urljoin(base_url, path)
                response = requests.get(url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    return response.text
                # Added small delay between requests to avoid errors
                time.sleep(0.5)
                
            except requests.exceptions.RequestException:
                continue
                
        return None
    except Exception as e:
        return f"Error fetching API docs: {str(e)}"

