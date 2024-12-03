import json
import urllib.request as request
from urllib.parse import urlparse

ALLOWED_HOSTS = ['example.com', 'api.example.com']  # Define the allowed hosts

def is_allowed_url(url):
    """
    Check if the URL belongs to the allowed set of URLs.
    """
    parsed_url = urlparse(url)
    return parsed_url.hostname in ALLOWED_HOSTS

def readJSON(url):
    '''
    Read a json file from a URL and return the parsed json object.
    '''
    # Validate the URL to ensure it's in the allowed list
    if not is_allowed_url(url):
        raise ValueError("The URL provided is not allowed.")
    
    # Open the URL safely
    with request.urlopen(url) as response:
        # Ensure the response has a valid JSON content-type
        if 'application/json' not in response.getheader('Content-Type'):
            raise ValueError("The URL did not return a JSON response.")
        
        # Read the response data
        data = response.read()
        
        # Decode the data using the correct encoding
        encoding = response.info().get_content_charset('utf-8')
        json_data = json.loads(data.decode(encoding))
        
        return json_data

# Example usage:
try:
    url = 'https://api.example.com/data.json'
    data = readJSON(url)
    print(data)
except ValueError as e:
    print(e)

app = Flask(__name__)
app.config['DEBUG'] = False

app.config['SESSION_COOKIE_HTTPONLY'] = True

