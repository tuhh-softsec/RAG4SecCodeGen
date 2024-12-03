import json
import urllib.request as request
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse
import ssl
import re

# Custom exceptions for better error handling
class InvalidURLException(ValueError):
    pass

class ResponseTooLargeException(ValueError):
    pass

class ContentValidationException(ValueError):
    pass

class RedirectionException(ValueError):
    pass

def is_valid_url(url):
    try:
        result = urlparse(url)
        # Restrict scheme to 'https' only for secure connections
        if result.scheme != 'https' or not result.netloc:
            return False
        # Sanitize the URL to prevent potential exploits
        sanitized_url = re.sub(r"[^\w\s.-]", "", url)
        return sanitized_url == url
    except ValueError:
        return False

def readJSON(url, max_size=1048576, max_redirects=5):
    '''
    Read a json file from a secure URL and return the parsed json object.
    '''
    if not is_valid_url(url):
        raise InvalidURLException("Invalid URL provided.")

    # Create an SSL context that verifies the host certificate
    context = ssl.create_default_context()
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED

    # Ensure that the Python environment has up-to-date root certificates
    context.load_default_certs()

    try:
        # Open the URL with a timeout and read the response
        with request.urlopen(url, context=context, timeout=10) as response:
            if response.geturl() != url:
                # Check if redirection occurred and if it's still HTTPS
                if not is_valid_url(response.geturl()) or response.redirect_dict > max_redirects:
                    raise RedirectionException("Redirection to an invalid or insecure URL detected.")
            # Limit the size of the response to prevent DoS attacks
            source = response.read(max_size)
            if len(source) == max_size:
                raise ResponseTooLargeException("Response too large.")
            if response.getcode() == 200:
                data = json.loads(source)
                # Perform content validation here if necessary
                # ...
                return data
            else:
                raise ValueError(f"Server responded with status code: {response.getcode()}")
    except HTTPError as e:
        raise ValueError(f"HTTP error occurred: {e.code} - {e.reason}")
    except URLError as e:
        if isinstance(e.reason, ssl.SSLError) and e.reason.reason == "CERTIFICATE_VERIFY_FAILED":
            raise ValueError("SSL certificate verification failed.")
        raise ValueError(f"URL error occurred: {e.reason}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {e.msg}")
    except Exception as e:
        # Avoid leaking information in error messages
        raise ValueError("An unexpected error occurred.")

# Example usage:
# try:
#     json_data = readJSON('https://example.com/data.json')
#     print(json_data)
# except ValueError as e:
#     print(f"Error: {e}")

