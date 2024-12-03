from flask import Flask, request, redirect, url_for, abort, make_response
from urllib.parse import urlparse, urljoin
import re
import logging

app = Flask(__name__)

# Configuration settings
BASE_URL = 'https://example.com'
app.secret_key = 'your-secret-key'  # Replace with a real secret key
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Regular expression pattern for allowed paths
ALLOWED_PATHS_REGEX = r'^/[\w/]+$'  # Tailor this regex to your application's requirements

# Function to check if the URL is safe for redirects
def is_safe_url(target):
    ref_url = urlparse(BASE_URL)
    test_url = urlparse(urljoin(BASE_URL, target))
    
    # Check if the scheme is 'https' for secure communication
    is_https = test_url.scheme == 'https'
    
    # Check if the domain is exactly the same, preventing subdomain trickery
    is_same_domain = ref_url.netloc == test_url.netloc
    
    # Additional pattern validation for the URL
    is_valid_pattern = re.match(ALLOWED_PATHS_REGEX, target) is not None
    
    return is_https and is_same_domain and is_valid_pattern

@app.route('/')
def index():
    # Get the next_url from the query string
    next_url = request.args.get('next_url', None)
    
    # Check if the next_url is provided and is safe
    if next_url and is_safe_url(next_url):
        return redirect(next_url)
    else:
        # Provide user feedback with a safe link back to the homepage
        response = make_response("The requested redirect was not allowed. Please <a href='/'>click here</a> to return to the homepage.", 400)
        return response

@app.errorhandler(404)
def page_not_found(e):
    # Custom 404 error page
    return "Page not found. Please return to the <a href='/'>homepage</a>.", 404

@app.errorhandler(500)
def internal_server_error(e):
    # Custom 500 error page
    return "An internal server error occurred. Please return to the <a href='/'>homepage</a>.", 500

# Set up logging
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    # Ensure debug mode is off in production
    app.run(debug=False, ssl_context='adhoc')  # Use 'adhoc' for self-signed cert or provide your own cert

