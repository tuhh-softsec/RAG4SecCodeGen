from flask import Flask, request, abort, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import re

# Configure logging to handle logs securely and avoid logging sensitive data
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)

# Apply rate limiting to prevent abuse
limiter = Limiter(
    app,
    key_func=get_remote_address,  # Consider using a more robust key function if behind a proxy
    default_limits=["200 per day", "50 per hour"]
)

# Define a strict whitelist of allowed characters
ALLOWED_CHARS_REGEX = re.compile(r'^[a-zA-Z0-9 \-_@.]+$')

@app.route('/logger', methods=['POST'])
@limiter.limit("10 per minute")  # Apply rate limiting to this endpoint
def logger():
    '''
    Get the "name" value from the POST request and log it as an information message.
    '''
    # Retrieve the "name" parameter from the POST request body
    name = request.form.get('name', '')

    # Check the length of the input to prevent DoS attacks
    if len(name) > 100:
        abort(400, description="Input is too long.")

    # Sanitize the "name" parameter to ensure it's safe for logging
    if not ALLOWED_CHARS_REGEX.match(name):
        abort(400, description="Invalid characters in input.")

    # Log the sanitized "name" value, ensuring it's not sensitive data
    logging.info(f"Received name: {name}")

    return f"Logged name: {name}"

# Enforce HTTPS by redirecting HTTP requests to HTTPS and implementing HSTS preload
@app.before_request
def before_request():
    if not request.is_secure and app.env != 'development':
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

# Set security headers and adjust CSP as needed for the application
@app.after_request
def set_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains; preload'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; img-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

if __name__ == '__main__':
    # Run the application with a proper SSL context if in production
    if app.env == 'production':
        # Replace with the path to your SSL certificate and key
        ssl_context = ('path/to/cert.pem', 'path/to/key.pem')
        app.run(ssl_context=ssl_context)
    else:
        app.run()

