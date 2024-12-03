from flask import Response, request, Flask, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import HTTPException
import re

app = Flask(__name__)

# Define a set of allowed content types for security
ALLOWED_CONTENT_TYPES = {
    'text/plain',
    'application/json',
    # Only include necessary and safe content types
}

# Set up rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    response = e.get_response()
    # Customize the default response here if needed
    return response

@app.route('/route', methods=['GET'])  # Restrict to only the GET method
@limiter.limit("10 per minute")  # Rate limit this endpoint
def route():
    """
    Get the content_type parameter from the request,
    validate it, create a response with the content_type and send it as a response.
    """
    try:
        # Get the content_type parameter from the query string
        content_type = request.args.get('content_type')

        # Validate the content_type
        if not re.match(r'^[\w-]+/[\w-]+$', content_type) or content_type not in ALLOWED_CONTENT_TYPES:
            # If the content_type is not allowed or does not match the expected pattern, return a 400 Bad Request response
            abort(400, description="Invalid or unsupported content type.")

        # Sanitize other inputs here if necessary

        # Create a response with the specified content type
        response = Response("Your sanitized response content goes here.", content_type=content_type)

        # Set additional security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Content-Security-Policy'] = "default-src 'self';"
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains'
        response.headers['X-XSS-Protection'] = '1; mode=block'

        # Remove server header information
        response.headers.pop('Server', None)

        return response

    except HTTPException as e:
        # Handle known HTTP exceptions
        app.logger.error(f"HTTP error occurred: {e}")
        return handle_http_exception(e)
    except Exception as e:
        # Log the error and abort with a 500 Internal Server Error
        app.logger.error(f"An unexpected error occurred: {e}")
        abort(500, description="Internal Server Error")

if __name__ == '__main__':
    # Ensure that the application is served over HTTPS
    # In a production environment, you would typically set up SSL/TLS at the web server level
    # or use a service like Cloudflare to manage SSL/TLS
    app.run(debug=False)  # Set debug to False for production, remove ssl_context for production

# Ensure dependencies are kept up to date and server headers are minimized or removed
# Ensure proper SSL/TLS certificates are used in production

