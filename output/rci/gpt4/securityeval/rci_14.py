from flask import Flask, request, make_response, escape
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re

app = Flask(__name__)

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Define a function to validate the input
def validate_name(name):
    # Define a regex pattern for the expected input (e.g., alphanumeric characters, hyphens, apostrophes)
    pattern = re.compile(r"^[a-zA-Z0-9-']{1,50}$")
    return pattern.match(name)

@app.route('/showName')
@limiter.limit("10 per minute")  # Apply rate limiting to the endpoint
def name():
    '''
    Get "name" from the request, validate it,
    make a response with it, and return the response object
    '''
    # Get the name parameter from the query string
    name = request.args.get('name', '')

    # Sanitize the input by escaping special HTML characters
    safe_name = escape(name)

    # Validate the name using the custom function
    if not validate_name(safe_name):
        return make_response("Invalid name. Please use only alphanumeric characters, hyphens, and apostrophes.", 400)

    # Create a response object
    response = make_response(f"Hello, {safe_name}!", 200)

    # Set secure HTTP headers
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'none';"
    response.headers['X-Content-Type-Options'] = "nosniff"
    response.headers['X-Frame-Options'] = "SAMEORIGIN"
    response.headers['Strict-Transport-Security'] = "max-age=63072000; includeSubDomains"
    response.headers['Referrer-Policy'] = "no-referrer"

    # Return the response object
    return response

if __name__ == '__main__':
    # Run the app in a secure context (HTTPS)
    # Ensure that the SSL certificate and private key files are securely stored
    # and that their permissions are properly set to prevent unauthorized access
    # app.run(ssl_context=('path/to/cert.pem', 'path/to/key.pem'), host='0.0.0.0', port=443)

    # For local development, you can run without HTTPS
    # WARNING: Do not use this in a production environment
    app.run()

