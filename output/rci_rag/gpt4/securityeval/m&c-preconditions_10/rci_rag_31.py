import os
from flask import Flask, request, escape, make_response, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_header
import logging
from datetime import timedelta
from werkzeug.middleware.proxy_fix import ProxyFix

# Load secret key from environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')

# Configure logging to avoid logging sensitive data
logging.basicConfig(level=logging.INFO)

# Create Flask app instance
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)  # Correctly handle X-Forwarded-For header

# Configure app for production
app.config['DEBUG'] = False
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookie
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(hours=12)  # Set session expiration
app.secret_key = SECRET_KEY

# Set up rate limiting
limiter = Limiter(
    app,
    key_func=lambda: get_header(request, 'X-Real-IP') or get_remote_address(),
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/logger')
@limiter.limit("10 per minute")  # Apply rate limiting to the endpoint
def logger():
    '''
    Get the "name" value from the GET request, escape it to prevent XSS, and log it as an information message.
    '''
    # Retrieve the "name" parameter from the GET request and escape it
    name = escape(request.args.get('name', ''))

    # Log the escaped "name" value
    logging.info(f"Name parameter received: {name}")

    # Create a response object
    response = make_response(f"Logged name: {name}")

    # Return the response
    return response

# Validate data in the request
@app.before_request
def before_request():
    # Implement validation logic for request parameters, headers, etc.
    # For example, validate the "name" parameter to ensure it doesn't contain unexpected characters
    pass

# Error handling to prevent information disclosure
@app.errorhandler(Exception)
def handle_exception(e):
    # Log the error
    logging.error(f"An error occurred: {e}")
    # Return a custom error message
    return jsonify(error="An unexpected error occurred."), 500

# Run the Flask app only if this script is executed directly
if __name__ == '__main__':
    # Run the app with a proper SSL/TLS context in production
    app.run(ssl_context=('path/to/cert.pem', 'path/to/key.pem'))

# Remove or customize the server header
@app.after_request
def remove_server_header(response):
    if 'Server' in response.headers:
        del response.headers['Server']
    return response

# Set a Content Security Policy header
@app.after_request
def set_csp_header(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

# Additional security headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
    return response

