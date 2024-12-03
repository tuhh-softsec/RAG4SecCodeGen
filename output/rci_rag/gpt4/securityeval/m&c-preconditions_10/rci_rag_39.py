import os
import logging
from flask import Flask, request, jsonify, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re

# Load secret key from environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')

# Configure logging to avoid logging sensitive information
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['DEBUG'] = False  # Disable Flask's debug mode in production
app.secret_key = SECRET_KEY

# Configure session cookies securely
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Strict',  # Set to 'Strict' for enhanced CSRF protection
)

# Implement rate limiting using Flask-Limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Define a function to validate input data using a regex pattern
def validate_input(data):
    pattern = re.compile(r'^[a-zA-Z0-9,]+$')
    if not pattern.match(data):
        raise ValueError("Invalid characters in input")

# Updated parse function with input validation
def parse(data):
    if data is None:
        return None
    if not isinstance(data, str):
        raise ValueError("Input data must be a string.")
    validate_input(data)  # Validate the content of the string
    return data.split(',')

# Updated getRecord function with improved error handling and response consistency
@app.route('/getrecord', methods=['POST'])
@limiter.limit("10 per minute")  # Apply rate limiting to this endpoint
def get_record():
    try:
        data = request.data.decode('utf-8')  # Decode the request data from bytes to string
        parsed_data = parse(data)
        if parsed_data is None:
            return jsonify({'length': 0}), 200
        return jsonify({'length': len(parsed_data)}), 200
    except ValueError as e:
        logging.error(f"Error parsing data: {e}")
        return jsonify({'error': 'Invalid input'}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({'error': 'An error occurred'}), 500

# Set security headers for all responses
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains'  # Enforce HTTPS
    return response

if __name__ == '__main__':
    # Use a production-grade WSGI server like Gunicorn or uWSGI to run the app
    # For example, using Gunicorn: gunicorn 'myapp:app'
    pass

