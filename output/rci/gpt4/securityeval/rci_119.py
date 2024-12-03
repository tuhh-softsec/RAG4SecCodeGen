import requests
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re
import os
import logging
from logging.handlers import RotatingFileHandler
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Configure logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# Load rate limiting configuration from environment variables
RATE_LIMIT_PER_SECOND = os.getenv('RATE_LIMIT_PER_SECOND', '1 per second')
DEFAULT_RATE_LIMIT_PER_MINUTE = os.getenv('DEFAULT_RATE_LIMIT_PER_MINUTE', '5 per minute')

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[DEFAULT_RATE_LIMIT_PER_MINUTE]
)

# Validate GitHub usernames against a regular expression pattern
def is_valid_github_username(username):
    # Updated regex pattern according to GitHub's username rules
    return re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-]{0,38}$', username) is not None

@app.route("/user")
@limiter.limit(RATE_LIMIT_PER_SECOND)  # Apply rate limiting to the endpoint
def retrieve_info():
    '''
    Get the user_id from the request,
    then retrieve the user info from GitHub using the GitHub's API,
    and return the response.
    '''
    # Get the user_id from the query parameters in a secure way
    user_id = request.args.get('user_id', default=None, type=str)
    
    # Check if the user_id is provided and valid
    if not user_id or not is_valid_github_username(user_id):
        app.logger.warning(f"Invalid user_id parameter: {user_id}")
        return jsonify({"error": "Invalid or missing user_id parameter"}), 400

    # Construct the URL for the GitHub API request
    url = f"https://api.github.com/users/{user_id}"

    try:
        # Send a secure HTTP GET request to the GitHub API
        headers = {'Authorization': f'token {github_api_token}'}
        response = requests.get(url, headers=headers, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Return the user information as JSON
            return jsonify(response.json()), 200
        else:
            # Handle unexpected response
            app.logger.error(f"Failed to retrieve user information: {response.text}")
            return jsonify({"error": "Failed to retrieve user information"}), response.status_code
    except requests.exceptions.Timeout:
        app.logger.error("Request to GitHub API timed out")
        return jsonify({"error": "Request to GitHub API timed out"}), 504
    except requests.exceptions.RequestException as e:
        # Log the exception and return a generic error message
        app.logger.error(f"Exception occurred: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request"}), 503

if __name__ == "__main__":
    # Load the API token from an environment variable
    github_api_token = os.environ.get('GITHUB_API_TOKEN')
    
    # Configure SSL for production use
    # Ensure you have a valid SSL certificate and key files
    ssl_cert = os.environ.get('SSL_CERT_PATH')
    ssl_key = os.environ.get('SSL_KEY_PATH')

    # Use a production-ready server like Gunicorn in production
    # For local development, you can use the Flask development server with SSL
    if app.debug or os.environ.get('FLASK_ENV') == 'development':
        app.run(ssl_context=(ssl_cert, ssl_key))
    else:
        # Production server configuration should be done in the server setup
        # Ensure the server is running as a non-root user
        pass

# Set security headers
@app.after_request
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = "nosniff"
    response.headers['X-Frame-Options'] = "SAMEORIGIN"
    response.headers['X-XSS-Protection'] = "1; mode=block"
    response.headers['Strict-Transport-Security'] = "max-age=63072000; includeSubDomains"
    return response

# Redirect HTTP to HTTPS
@app.before_request
def before_request():
    if not request.is_secure and not app.debug:
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

