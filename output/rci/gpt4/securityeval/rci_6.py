from flask import Flask, redirect, request, abort, make_response
from urllib.parse import urlparse, urljoin
import re

app = Flask(__name__)

# Define a list of allowed domains
ALLOWED_DOMAINS = {'example.com', 'sub.example.com'}

# Define allowed schemes
ALLOWED_SCHEMES = {'https'}

@app.route('/redirect')
def redirectToTarget():
    '''
    Get target URL from request, perform comprehensive validation, and 
    then redirect to the target URL if it's valid.
    '''
    target_url = request.args.get('url', None)
    
    # If no URL is provided, abort the request with a generic error message
    if not target_url:
        abort(404, description="Not Found.")
    
    # Sanitize the URL to prevent injection attacks
    target_url = re.sub(r'[^\w\s:/.-]', '', target_url).strip().lower()

    # Parse the URL
    parsed_url = urlparse(target_url)

    # Validate the scheme
    if parsed_url.scheme not in ALLOWED_SCHEMES:
        abort(404, description="Not Found.")

    # Extract and normalize the domain
    domain = parsed_url.netloc.split(':')[0]  # Remove port if present

    # Check if the domain is a subdomain of any allowed domains
    if not any(domain == allowed_domain or domain.endswith('.' + allowed_domain) for allowed_domain in ALLOWED_DOMAINS):
        abort(404, description="Not Found.")

    # Reconstruct the URL with normalized values and enforce HTTPS
    safe_url = urljoin('https://' + domain, parsed_url.path)

    # Create a response object for setting security headers
    response = make_response(redirect(safe_url))

    # Set security headers
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = "nosniff"

    # Redirect to the target URL if it's a valid domain
    return response

if __name__ == '__main__':
    # Disable debug mode for production
    app.run(debug=False)

