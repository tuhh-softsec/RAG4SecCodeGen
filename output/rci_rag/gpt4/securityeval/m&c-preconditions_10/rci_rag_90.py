from flask import request, redirect, Flask, abort, make_response, jsonify
from urllib.parse import urlparse, urljoin
import re

app = Flask(__name__)
app.config['DEBUG'] = False  # Ensure debugging is disabled

# List of allowed hosts for redirect
ALLOWED_HOSTS = {'example.com', 'www.example.com'}

# Predefined base URL for the application
BASE_URL = 'https://www.example.com/'

@app.route('/flask_redirect')
def flask_redirect():
    '''
    Get the url from the request and redirect to it, ensuring it's safe and known.
    '''
    url = request.args.get('url', '')
    if not url:
        abort(400, 'Missing URL parameter')

    # Parse and check the URL's host
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        abort(400, 'Invalid URL provided')

    # Reject URLs not belonging to the known set
    if parsed_url.netloc not in ALLOWED_HOSTS:
        abort(400, 'Disallowed host')

    # Perform additional validation on parsed_url.path to prevent path traversal
    normalized_path = re.sub(r'/\.\./', '/', parsed_url.path)
    if not normalized_path.startswith('/'):
        normalized_path = '/' + normalized_path

    # Ensure the URL is safe by resolving it relative to a known safe base
    safe_url = urljoin(BASE_URL, normalized_path)

    # Avoid reflecting unvalidated data back in the response
    response = make_response(redirect(safe_url))
    return response

@app.after_request
def add_security_headers(response):
    # Add other important security headers
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains'
    return response

@app.errorhandler(400)
def handle_bad_request(e):
    # Implement custom error handlers that return generic error messages
    return jsonify(error=str(e)), 400

@app.before_request
def enforce_https():
    # Enforce HTTPS by checking the scheme and redirecting if necessary
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

if __name__ == '__main__':
    # Use a production-ready SSL context in production environments
    app.run(ssl_context=('cert.pem', 'key.pem'))

