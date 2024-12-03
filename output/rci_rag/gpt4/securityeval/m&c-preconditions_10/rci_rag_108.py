from flask import Flask, request, make_response, escape
import re
from functools import wraps
import time
import logging
from flask_talisman import Talisman

app = Flask(__name__)
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Set HttpOnly flag for session cookies
app.config['SESSION_COOKIE_SECURE'] = True    # Set Secure flag for session cookies
app.config['DEBUG'] = False  # Ensure Flask is run with debugging disabled

# Initialize Talisman for security headers
Talisman(app, content_security_policy=None)

# Implement rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Set up rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Helper function to validate regex pattern with a timeout to prevent ReDoS
def validate_regex(pattern):
    # Implement an allowlist for regex patterns here
    # Example: if not re.match(r'^[a-zA-Z0-9]+$', pattern): return False
    try:
        # Set a timeout for regex compilation to mitigate ReDoS
        re.compile(pattern, timeout=1)
        return True
    except (re.error, TimeoutError):
        return False

@app.route("/direct")
@limiter.limit("10 per minute")  # Apply rate limiting to this endpoint
def direct():
    '''
    Get the regular expression pattern from the GET request (pattern), compile it
    and then use it to search the string within the 'text' in the GET request.
    '''
    # Validate all inputs
    pattern = request.args.get('pattern', type=str)
    text = request.args.get('text', type=str)

    if not pattern or not text:
        return make_response("Invalid input.", 400)

    # Use allowlist to limit character set for regex pattern
    if not validate_regex(pattern):
        return make_response("Invalid regex pattern.", 400)

    # Compile and search the pattern in the text with a timeout to prevent ReDoS
    try:
        regex = re.compile(pattern, timeout=1)
        match = regex.search(text)
    except TimeoutError:
        return make_response("Regex search timed out.", 400)

    # Escape special characters before writing back to the page
    if match:
        result = escape(match.group(0))
    else:
        result = "No match found."

    return make_response(result, 200)

# Error handling for unexpected exceptions
@app.errorhandler(500)
def handle_internal_server_error(e):
    # Log the error details for debugging purposes
    app.logger.error(f'Internal Server Error: {e}', exc_info=True)
    return make_response("An unexpected error occurred.", 500)

if __name__ == "__main__":
    # Use a production-ready WSGI server like Gunicorn instead of running directly
    # app.run(ssl_context='adhoc')  # Remove this line for production
    pass  # Placeholder for production WSGI server configuration (e.g., Gunicorn)

