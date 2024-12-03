from flask import Flask, redirect, request, abort, session
from flask_wtf.csrf import CSRFProtect
from urllib.parse import urlparse
import os

app = Flask(__name__)

# Load the secret key from an environment variable or a file
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'default-secret-key'

# Ensure cookies are sent over HTTPS and prevent JavaScript access to session cookie
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize CSRF protection
csrf = CSRFProtect(app)

# List of known valid URLs for redirection
VALID_URLS = ['example.com']

@app.route('/redirect')
def redirectToTarget():
    target_url = request.args.get('url', '')
    if not target_url:
        abort(400, description="Missing URL parameter")

    # Parse the URL before checking its host value
    parsed_url = urlparse(target_url)

    # Check for an exact match or a proper subdomain structure
    if not any(parsed_url.netloc == valid_url or parsed_url.netloc.endswith('.' + valid_url) for valid_url in VALID_URLS):
        abort(400, description="Invalid URL")

    # Redirect to the target URL if all checks pass
    response = redirect(target_url)

    # Implement a Content Security Policy (CSP) that matches the application's needs
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; object-src 'none';"

    return response

# Custom error handlers to ensure user-friendly error messages
@app.errorhandler(400)
def handle_bad_request(e):
    return 'Bad request! Please check your URL.', 400

@app.errorhandler(403)
def handle_forbidden(e):
    return 'Forbidden! You do not have permission to access this resource.', 403

# Implement rate limiting using extensions like Flask-Limiter
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
# limiter = Limiter(app, key_func=get_remote_address)
# Apply rate limits to routes as needed

# Set up logging and monitoring according to the deployment environment
# import logging
# logging.basicConfig(level=logging.INFO)

# Ensure HTTPS is enforced in the production environment
# This can be done using a reverse proxy or within the application itself

# Input validation and sanitization should be implemented as needed

# Keep dependencies up to date and monitor them for vulnerabilities
# Use tools like pip-audit or safety to check for known vulnerabilities

if __name__ == '__main__':
    # Do not use app.run() for production deployments
    # Instead, use a production-ready WSGI server like Gunicorn or uWSGI
    # and run the application behind a reverse proxy like Nginx
    app.run(ssl_context='adhoc')  # For local development only

