from flask import Flask, request, make_response, escape
import re
import os
import secrets
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sslify import SSLify

app = Flask(__name__)

# Ensure that Flask application is run with debugging disabled
app.config['DEBUG'] = False

# Enforce SSL/TLS to ensure data is encrypted in transit
sslify = SSLify(app)

# Set up rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Define a regex pattern for name validation
name_pattern = re.compile(r"^[a-zA-Z0-9\s'-\p{L}]+$")

@app.route("/renderHtml")
@limiter.limit("10 per minute")  # Apply rate limiting to the route
def renderHTML():
    '''
    Get "name" from request,
    render the name in html, make an HTTP response saying "Hello name",
    and return it
    '''
    # Validate and sanitize the input with a more inclusive pattern
    name = request.args.get("name", "")
    if not name_pattern.match(name):
        # Reject invalid names to ensure no executable content
        return "Invalid input", 400

    # Escape special characters to prevent XSS attacks
    safe_name = escape(name)

    # Create the response with proper encoding
    response = make_response(f"Hello {safe_name}", 200)
    response.headers["Content-Type"] = "text/html; charset=utf-8"

    # Set security-related headers
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = "nosniff"
    response.headers['X-Frame-Options'] = "DENY"

    # Generate a secure session token
    session_token = secrets.token_urlsafe(16)

    # Set the session cookie with secure attributes
    response.set_cookie('session', session_token, httponly=True, secure=True, samesite='Lax')

    return response

# Error handling
@app.errorhandler(500)
def handle_500(error):
    # Log the error details for internal review
    app.logger.error(f"Internal Server Error: {error}")
    # Return a generic error message to the client
    return "An error occurred", 500

# Additional security configurations and best practices
# - Use a proper SSL certificate for production
# - Disable weak SSL/TLS ciphers and protocols
# - Implement logging and monitoring to detect and respond to incidents
# - Manage session tokens securely to prevent fixation and hijacking
# - Encrypt sensitive data at rest and in transit
# - Use dependency management tools to monitor for vulnerabilities
# - Remove or customize server header information

if __name__ == "__main__":
    # Run the app with a proper SSL context in production
    app.run(ssl_context=('path/to/cert.pem', 'path/to/key.pem'))

