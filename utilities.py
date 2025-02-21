import requests
import time
from urllib.parse import urljoin
import re


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



def extract_python_code(input_text):
    # Match Python code blocks

    code_blocks = re.findall(r'```python(.*?)```', input_text, re.DOTALL)
    
    if code_blocks:
        clean_code = '\n'.join(code_blocks).strip()
        return clean_code.replace("°", " ")
    else:
        if "python" in input_text:
            re.sub(r'^(?i).*python.*\n?', '', input_text, count=1)
        return input_text
