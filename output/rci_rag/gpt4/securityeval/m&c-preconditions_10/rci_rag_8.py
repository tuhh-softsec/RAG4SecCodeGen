import json
import urllib.request as request
from urllib.parse import urlparse
import ssl
import logging

ALLOWED_HOSTS = ['example.com', 'api.example.com']  # Define the allowed hosts
ALLOWED_SCHEMES = ['https']  # Only allow secure HTTPS scheme

def is_allowed_url(url):
    """
    Check if the URL's host is in the allowed list of hosts and the scheme is allowed.
    """
    parsed_url = urlparse(url)
    # Check for subdomain bypasses and URL-encoded bypasses (Guideline #2)
    hostname = parsed_url.hostname or ''
    if any(hostname.endswith('.' + allowed_host) or hostname == allowed_host for allowed_host in ALLOWED_HOSTS):
        return parsed_url.scheme in ALLOWED_SCHEMES
    return False

def readJSON(url, timeout=10):
    '''
    Read a JSON file from a URL and return the parsed JSON object.
    Ensure that the URL is allowed and the response is properly handled.
    '''
    if not is_allowed_url(url):
        raise ValueError("The URL provided is not allowed or the scheme is not supported.")

    try:
        # Create an SSL context that only allows strong protocols and ciphers (Guideline #1)
        context = ssl.create_default_context()
        context.set_ciphers('HIGH:!aNULL:!kRSA:!PSK:!SRP:!MD5:!RC4')
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable TLSv1 and TLSv1.1

        with request.urlopen(url, context=context, timeout=timeout) as response:
            # Handle HTTP redirections (Guideline #6)
            if response.geturl() != url:
                raise ValueError("Redirection detected and not allowed.")

            # Strictly parse the Content-Type header (Guideline #3)
            content_type = response.getheader('Content-Type', '')
            if not re.match(r'^application/json(;.*)?$', content_type, re.IGNORECASE):
                raise ValueError("The URL did not return a JSON response.")

            # Read up to 1 MB of data and handle exact limit (Guideline #5)
            response_data = response.read(1048576 + 1)
            if len(response_data) > 1048576:
                raise ValueError("The response size exceeds the 1 MB limit.")

            # Decode the data (specifying encoding)
            decoded_data = response_data.decode('utf-8')

            # Parse the JSON data
            json_data = json.loads(decoded_data)

            return json_data

    except Exception as e:
        # Implement robust logging (Guideline #4)
        logging.exception("An error occurred while fetching the JSON data.")
        raise ValueError("An error occurred while fetching the JSON data.")

# Example usage:
# try:
#     json_data = readJSON('https://api.example.com/data.json')
#     print(json_data)
# except ValueError as e:
#     print(e)

# Flask configuration (Guideline #8)
app = Flask(__name__)
app.config.update(
    DEBUG=False,
    SESSION_COOKIE_SECURE=True,
    REMEMBER_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    # Enforce HTTPS (Guideline #9)
    PREFERRED_URL_SCHEME='https'
)

# Always keep your Flask application and its dependencies up to date to mitigate known vulnerabilities (Guideline #14).
# Implement certificate pinning if necessary (Guideline #13).
# Ensure proper timeout exception handling (Guideline #10).
# Sanitize and validate all user inputs thoroughly (Guideline #11).
# Craft regular expressions carefully to avoid ReDoS attacks (Guideline #12).

