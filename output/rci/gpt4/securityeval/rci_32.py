from flask import Flask, request, abort, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from logging.handlers import RotatingFileHandler
import os
import re
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Configure rate limiting with a more sophisticated key function if necessary
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Configure logging
log_directory = 'logs'
log_file = 'application.log'
if not os.path.exists(log_directory):
    os.mkdir(log_directory)
    os.chmod(log_directory, 0o750)  # Set directory permissions to allow owner access
file_handler = RotatingFileHandler(os.path.join(log_directory, log_file), maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# Set file permissions to read/write for owner and read for group
os.chmod(os.path.join(log_directory, log_file), 0o640)

@app.errorhandler(HTTPException)
def handle_exception(e):
    # Log the error including the stack trace
    app.logger.error(f'HTTPException: {e}', exc_info=True)
    # Return JSON error response
    response = e.get_response()
    response.data = jsonify(code=e.code, name=e.name, description=e.description)
    response.content_type = "application/json"
    return response

@app.route('/log')
@limiter.limit("10 per minute")  # Rate limit to protect against DoS attacks
def log():
    user_input = request.args.get('input', '')  # Default to empty string if 'input' not provided

    # Validate the input against expected patterns or data types
    if not validate_input(user_input):
        app.logger.warning(f'Invalid input: {user_input}')
        abort(400)  # Bad request if input is not valid

    # Sanitize the input to prevent injection attacks
    sanitized_input = sanitize_input(user_input)

    # Log the sanitized input at an appropriate logging level
    app.logger.info(f'User input: {sanitized_input}')

    return 'Input logged', 200

def validate_input(input_str):
    # Define a validation pattern for the input, e.g., alphanumeric with specific symbols
    # This pattern should be adjusted according to the expected input
    pattern = re.compile(r'^[a-zA-Z0-9\s.,!?-]*$')
    return pattern.match(input_str) is not None

def sanitize_input(input_str):
    # Implement comprehensive sanitization based on the context
    # This might include escaping or removing special characters, encoding, etc.
    # The following is a simple example and should be tailored to your needs
    sanitized = re.sub(r'[^a-zA-Z0-9\s.,!?-]', '_', input_str)  # Replace unexpected chars with underscore
    return sanitized

if __name__ == '__main__':
    # Do not use debug mode in production
    app.run(debug=False, ssl_context='adhoc')  # Use adhoc SSL context for HTTPS

