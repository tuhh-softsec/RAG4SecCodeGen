from flask import Flask, request, redirect, url_for, abort, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)

# Load allowed paths from a configuration file or environment variable
ALLOWED_PATHS = os.getenv('ALLOWED_PATHS', {
    'profile': '/profile',
    'dashboard': '/dashboard',
    # Add more predefined paths as needed
}).split(',')

# Set up rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Set up logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

@app.route('/set_location_header')
@limiter.limit("10 per minute")  # Apply rate limiting to the endpoint
def set_location_header():
    '''
    Get the "next" value from the request and set the location header for redirecting to the value of "next".
    Validate the "next" value to ensure it's a safe redirect within the same site.
    '''
    next_path = request.args.get('next', None)
    
    # Ensure the next_path is provided
    if not next_path:
        abort(400, description="Missing 'next' parameter for redirection")
    
    # Normalize and validate the next_path
    if next_path in ALLOWED_PATHS:
        next_url = url_for(ALLOWED_PATHS[next_path])
        return redirect(next_url)
    else:
        # Log the failed redirection attempt without sensitive information
        app.logger.warning(f"Unsafe redirect attempt detected for path: {secure_filename(next_path)}")
        # Provide a generic error message and a way to navigate back
        return abort(400, description="Invalid redirection attempt. Please return to the homepage.")

# Apply HTTPS enforcement
@app.before_request
def before_request():
    if not request.is_secure and app.env != 'development':
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

# Set security headers
@app.after_request
def set_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

if __name__ == '__main__':
    # Disable debug mode in production
    app.run(debug=False, ssl_context='adhoc')  # Use 'adhoc' for self-signed cert or provide your own

