from flask import Flask, request, abort, make_response, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re
from regex import compile as re_compile, TIMEOUT
import logging
from functools import wraps

app = Flask(__name__)
app.config['DEBUG'] = False  # Ensure debugging is disabled

# Configure logging
logging.basicConfig(level=logging.INFO)

# Implement rate limiting using Flask-Limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,  # Consider using a more granular key function
    default_limits=["200 per day", "50 per hour"]
)

# Set security-related HTTP headers using after_request
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains'
    del response.headers['Server']  # Remove the server header entirely
    return response

# Authorization decorator to check if a user is authorized
def require_authorization(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not user_is_authorized():
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

@app.route("/direct")
@limiter.limit("10 per minute")  # Apply rate limiting to this endpoint
@require_authorization  # Require user authorization
def direct():
    '''
    Get the regex from the 'pattern' in the GET request,
    get the 'text' from the GET request,
    and search the 'text' with the provided regex.
    '''
    # Validate the data in the request
    pattern = request.args.get('pattern', '')
    text = request.args.get('text', '')

    # Use a stringent allowlist to limit the character set for the pattern
    if not re.match(r'^[a-zA-Z0-9\\s]+$', pattern):
        abort(400, description='Invalid pattern')  # Bad Request due to invalid pattern

    # Sanitize the text input to prevent injection attacks
    # Implement text sanitization logic here based on your application's requirements

    # Sanitize the regex pattern to prevent ReDoS attacks
    try:
        # Compile the pattern with a shorter timeout to prevent long-running operations
        regex = re_compile(pattern, re.UNICODE | re.IGNORECASE, timeout=0.5)
    except TIMEOUT:
        abort(400, description='Regex pattern took too long to compile')  # Bad Request due to timeout
    except re.error:
        abort(400, description='Invalid regex pattern')  # Bad Request due to invalid regex pattern

    # Perform the regex search
    match = regex.search(text)
    if match:
        return jsonify({'message': 'Match found', 'match': match.group()})
    else:
        return jsonify({'message': 'No match found'})

def user_is_authorized():
    # Placeholder function for checking user authorization
    # Implement actual authorization logic here
    return True

# Custom error handler to ensure that error responses do not leak sensitive information
@app.errorhandler(Exception)
def handle_exception(e):
    # Log the exception
    logging.error(f'Unhandled exception: {e}')
    # Differentiate between types of errors
    if isinstance(e, HTTPException):
        return jsonify({'error': str(e)}), e.code
    return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == "__main__":
    # Use a production-ready WSGI server like Gunicorn or uWSGI in production
    # Ensure that the WSGI server is properly configured for security and performance
    app.run(ssl_context=('cert.pem', 'key.pem'))  # Use proper SSL context for HTTPS in production

