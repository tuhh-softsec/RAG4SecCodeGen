from flask import Flask, request, make_response, escape, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
import re
import os

app = Flask(__name__)

# Configure application for production environment
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Define a more comprehensive input validation function
def validate_username(username):
    # Add more sophisticated checks based on the application's requirements
    if not re.match("^[A-Za-z0-9]{3,20}$", username):
        return False
    # Additional checks can be added here (e.g., reserved usernames)
    return True

@app.errorhandler(404)
def page_not_found(e):
    # Generic error handling for 404
    return make_response("This page does not exist.", 404)

@app.errorhandler(500)
def internal_server_error(e):
    # Generic error handling for 500
    return make_response("An internal server error occurred.", 500)

@app.route("/profile")
@limiter.limit("5 per minute")  # Apply rate limiting to the endpoint
def profile():
    '''
    Get the username from the request, validate and sanitize it, 
    make a response with it and return it.
    '''
    # Assuming the username is passed as a query parameter
    username = request.args.get('username', '')

    # Validate and sanitize the input
    if not validate_username(username):
        # Return an error response if the username is invalid
        return make_response("Invalid username.", 400)

    # Escape the username to prevent XSS attacks
    safe_username = escape(username)

    # Create a response with the sanitized username
    response = make_response(f"Profile page for {safe_username}", 200)

    # Set security-related headers
    response.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self' https://trusted-site.com;"
    response.headers['X-Content-Type-Options'] = "nosniff"
    response.headers['X-Frame-Options'] = "SAMEORIGIN"
    response.headers['X-XSS-Protection'] = "1; mode=block"
    response.headers['Strict-Transport-Security'] = "max-age=63072000; includeSubDomains"

    # Ensure that cookies are set with secure flags
    session['username'] = safe_username  # Use Flask's session mechanism for secure cookie handling

    return response

# Additional routes and logic for authentication, authorization, and other application features would go here

if __name__ == "__main__":
    # Run the app with a production-ready server like Gunicorn or uWSGI
    # and behind a reverse proxy like Nginx or Apache in production environments.
    # The built-in Flask server is only for development purposes.
    # Example command to run with Gunicorn: gunicorn -b :5000 myapp:app
    app.run(ssl_context='adhoc')  # Use 'adhoc' for testing only, replace with proper SSL context in production

