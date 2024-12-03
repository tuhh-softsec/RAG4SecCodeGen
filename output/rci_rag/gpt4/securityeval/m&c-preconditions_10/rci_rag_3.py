from flask import Flask, request, make_response, escape, session, abort
import os
import re
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

app = Flask(__name__)

# Load the secret key from an environment variable and fail if not set
if 'SECRET_KEY' in os.environ:
    app.secret_key = os.environ['SECRET_KEY']
else:
    raise ValueError("No SECRET_KEY set for Flask application")

# Ensure that Flask application is run with debugging disabled
app.config['DEBUG'] = False

# Configure session cookie flags
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True  # Enforce HTTPS in production

# Implement rate limiting to prevent abuse
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Set a Content Security Policy
@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

# Custom error handler that logs errors
@app.errorhandler(500)
def handle_500_error(exception):
    app.logger.error(f"Internal server error: {exception}")
    return "An internal server error occurred.", 500

@app.errorhandler(404)
def handle_404_error(exception):
    app.logger.warning(f"Page not found: {exception}")
    return "Page not found.", 404

@app.route("/profile")
@limiter.limit("10 per minute")  # Apply rate limiting to the profile endpoint
def profile():
    '''
    Get the username from the request, make a response with it and return it
    '''
    # Validate the data in the request
    username = request.args.get('username', '')
    if not re.match(r'^[a-zA-Z0-9_]+$', username):  # Allowlist for username (alphanumeric and underscores)
        return "Invalid input provided.", 400

    # Store the raw username in the session
    session['username'] = username

    # Escape the input before writing user input to the page
    safe_username = escape(username)

    # Make a response with the safe username
    response = make_response(f"Hello, {safe_username}!")

    # Specify encoding in the HTTP header
    response.headers['Content-Type'] = 'text/html; charset=utf-8'

    return response

# Configure logging
logging.basicConfig(level=logging.INFO)

# Production server enforcement (example using Gunicorn)
# if __name__ == "__main__":
#     abort(500, description="This application must not be run using app.run() in a production environment.")

# Ensure to configure HTTPS enforcement in your production environment
# This can be done using a reverse proxy like Nginx or middleware that redirects HTTP to HTTPS

# Remember to manage your dependencies securely and keep them up to date
# Use tools like `pip-audit` to check for vulnerabilities in your dependencies

# Implement proper logging for monitoring and investigating security incidents
# Configure logging as needed for your application's requirements

# Additional security headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'no-referrer'
    return response

# Environment configuration distinction
if app.config['ENV'] == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

# Ensure that the application is not run with app.run() in a production environment
if __name__ == "__main__":
    if app.config['ENV'] == 'production':
        raise Exception("The application must not be run with app.run() in a production environment.")
    app.run()

