import requests
from urllib.parse import urlparse
from requests.exceptions import RequestException
import time
import os

# Load the list of allowed URLs from an environment variable or secure external source
ALLOWED_URLS = os.getenv('ALLOWED_URLS', 'https://semmle.com').split(',')

# Function to validate URL against the allowlist
def is_allowed_url(url):
    parsed_url = urlparse(url)
    # Validate the URL structure and content to prevent malformed URLs or dangerous characters
    return parsed_url.scheme in ('http', 'https') and parsed_url.netloc in ALLOWED_URLS

# Function to make a secure HTTP request with improved error handling and rate limiting
def make_secure_request(url):
    if not is_allowed_url(url):
        raise ValueError("URL is not allowed")

    headers = {'User-Agent': 'MyCustomUserAgent/1.0'}
    try:
        # Implement rate limiting using a simple sleep mechanism (for demonstration purposes)
        # In production, use a more sophisticated approach like a token bucket or leaky bucket algorithm
        time.sleep(1)  # Wait for 1 second before making a request

        response = requests.get(url, headers=headers, verify=True)

        if response.status_code == 200:
            # Securely process the response data
            pass
        elif response.status_code == 429:
            # Implement a backoff strategy
            time.sleep(10)  # Wait for 10 seconds before retrying
            return make_secure_request(url)  # Retry the request
        elif response.status_code >= 500:
            # Log server errors and consider retrying
            pass
        else:
            # Handle other errors appropriately
            pass

        return response
    except RequestException as e:
        # Handle exceptions from the requests library
        print(f"An error occurred: {e}")
        # Consider retrying or logging the error based on the exception type
    except Exception as e:
        # Handle any other exceptions
        print(f"An unexpected error occurred: {e}")

# Example usage
try:
    response = make_secure_request('https://semmle.com')
    if response:
        print(response.text)
except ValueError as e:
    print(e)

# Additional security considerations:
# - Implement certificate pinning for high-security applications.
# - Regularly update and monitor the 'requests' library for security vulnerabilities.
# - Load the ALLOWED_URLS list from a secure external source or configuration file.
# - Ensure that any data processing is done securely to prevent data leaks or injection attacks.
# - Set appropriate HTTP security headers if needed when making requests.
# - Manage API keys and sensitive data securely, avoiding hardcoding or logging them.
# - Ensure the underlying system has an up-to-date CA bundle for SSL certificate validation.

