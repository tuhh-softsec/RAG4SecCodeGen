from flask import Flask, redirect, request, abort, Response
from urllib.parse import urlparse, urljoin
import re

app = Flask(__name__)

# Define a whitelist of allowed domains
ALLOWED_DOMAINS = {'example.com', 'www.example.com'}

@app.after_request
def set_security_headers(response):
    # Set Content Security Policy (CSP)
    response.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self' https://trusted-images.example.com;"
    # Set X-Frame-Options to prevent clickjacking
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    # Remove server header information
    response.headers.pop('Server', None)
    return response

@app.route('/redirect')
def redirectToTarget():
    target_url = request.args.get('url', None)
    
    if target_url:
        # Ensure the base URL is the application's host URL
        base_url = request.host_url if request.host_url.startswith('https') else 'https://' + request.host.split(':')[0]
        # Normalize the URL only if it's a relative URL
        target_url = urljoin(base_url, target_url) if not urlparse(target_url).netloc else target_url
        parsed_url = urlparse(target_url)
    
    # Check if the URL is not provided, not HTTPS, or domain not in the whitelist
    if not target_url or parsed_url.scheme != 'https' or parsed_url.netloc not in ALLOWED_DOMAINS:
        # Log the error for monitoring without sensitive information
        app.logger.warning('Unsafe redirect attempt detected.')
        # Provide a generic error message to the end-user
        abort(400, description="Invalid request.")
    
    # If the URL is safe, proceed with the redirection
    return redirect(target_url)

if __name__ == '__main__':
    # Disable debug mode in production
    app.run(debug=False, ssl_context='adhoc')  # Use 'adhoc' for self-signed cert or provide a path to a valid cert

