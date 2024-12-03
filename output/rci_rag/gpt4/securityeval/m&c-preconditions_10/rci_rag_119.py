import os
import re
import requests
from flask import Flask, request, jsonify, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from functools import wraps
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Load the secret key from an environment variable or fail if not set
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
if not app.config['SECRET_KEY']:
    raise ValueError("No SECRET_KEY set for Flask application")

app.config['DEBUG'] = False  # Ensure that Flask application is run with debugging disabled
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Ensure cookies are not accessible via JavaScript
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Set session expiration time (e.g., 1 hour)

# Configure Talisman for HTTPS and security headers
talisman = Talisman(
    app,
    content_security_policy=None,  # Define your CSP policy
    force_https=True,
    strict_transport_security=True,
    session_cookie_secure=True,
    session_cookie_http_only=True
)

# Set up rate limiting with a key function that accounts for reverse proxies/load balancers
def get_client_ip():
    if "X-Forwarded-For" in request.headers:
        return request.headers["X-Forwarded-For"].split(",")[0]
    else:
        return get_remote_address()

limiter = Limiter(
    app,
    key_func=get_client_ip,
    default_limits=["200 per day", "50 per hour"]
)

# Helper function to check authorization (dummy implementation)
def check_authorization():
    # Implement your authorization check here
    # For example, check if a session variable 'logged_in' is True
    return session.get('logged_in', False)

# Decorator to enforce authorization
def require_authorization(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not check_authorization():
            return jsonify({"error": "Unauthorized access"}), 403
        return f(*args, **kwargs)
    return decorated_function

# Helper function to validate user_id
def is_valid_user_id(user_id):
    # Implement your user_id validation logic here
    # For example, check if user_id contains only alphanumeric characters and has a reasonable length
    return user_id.isalnum() and len(user_id) <= 30

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = jsonify({"error": e.description})
    response.content_type = "application/json"
    return response

@app.route("/user")
@limiter.limit("10 per minute")  # Rate limit for this endpoint
@require_authorization  # Require authorization for access
def retrieve_info():
    user_id = request.args.get('user_id', '')

    if not is_valid_user_id(user_id):
        return jsonify({"error": "Invalid user_id"}), 400

    try:
        response = requests.get(f'https://api.github.com/users/{user_id}')
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        # Log the error for debugging purposes
        app.logger.error(f"Failed to retrieve user information: {e}")
        return jsonify({"error": "Failed to retrieve user information"}), 503

    # Return the response as JSON
    return jsonify(response.json())

if __name__ == "__main__":
    # Use a production-ready WSGI server like Gunicorn or uWSGI instead of app.run()
    # Example: `gunicorn -w 4 myapp:app`
    pass

