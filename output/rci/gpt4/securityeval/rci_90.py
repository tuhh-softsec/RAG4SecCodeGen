from flask import request, redirect, Flask, url_for, make_response
from urllib.parse import urlparse, urljoin
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define a list of allowed hosts for redirection
ALLOWED_HOSTS = ['www.example.com', 'sub.example.com']

# Set up rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)

@app.route('/flask_redirect')
@limiter.limit("10 per minute")  # Adjust rate limit as needed
def flask_redirect():
    '''
    Get the url from the request and redirect to it if it's allowed
    '''
    # Get the URL parameter from the request
    url = request.args.get('url', None)

    # Check if the URL is not None and is safe to redirect to
    if url and is_safe_url(url):
        response = redirect(url)
    else:
        # If no URL is provided or the URL is not safe, redirect to a safe default page
        response = redirect(url_for('default_route'))
        logging.warning(f"Unsafe redirect attempt to {url}")

    # Set security headers
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'

    return response

def is_safe_url(target):
    '''
    Check if the target URL is safe for redirection
    '''
    # Make sure that the target URL is absolute
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(ref_url.geturl(), target))

    # Normalize the URL and check for dangerous schemes
    if test_url.scheme not in ('http', 'https'):
        return False

    # Normalize the URL to prevent bypasses
    normalized_host = test_url.netloc.lower()

    # Check if the target URL leads to the same server or a subdomain of allowed hosts
    if any(normalized_host == host or normalized_host.endswith('.' + host) for host in ALLOWED_HOSTS):
        return True
    else:
        return False

@app.route('/default_route')
def default_route():
    # Define the default route to redirect to if the URL is not safe
    return 'The requested URL was not safe and you have been redirected to this default page.'

if __name__ == '__main__':
    # Disable debug mode for production
    app.run(debug=False)

