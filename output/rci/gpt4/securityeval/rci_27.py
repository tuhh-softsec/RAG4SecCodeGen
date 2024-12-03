from flask import Flask, request, Response
import logging
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define a global exception handler
@app.errorhandler(Exception)
def handle_exception(e):
    # Log the exception details for debugging and auditing purposes
    app.logger.error(f"An internal error occurred: {e}", exc_info=True)
    
    if isinstance(e, HTTPException):
        return e
    return Response("An internal error occurred.", status=500, content_type='text/plain')

@app.route('/')
def route():
    # Get the content_type parameter from the request args or headers
    content_type = request.args.get('content_type', default='text/plain').lower().strip()
    
    # Validate the content_type to prevent content sniffing and other security issues
    # Here we only allow certain content types for security reasons
    allowed_content_types = ['text/plain', 'application/json', 'text/html']
    if content_type not in allowed_content_types:
        # If the content_type is not allowed, return a 400 Bad Request response
        return Response("Invalid content type requested.", status=400, content_type='text/plain')

    # Create a response with the specified content_type
    response = Response(f"Your content type is: {content_type}", content_type=content_type)

    # Set security-related headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self' https: data:; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains; preload'

    # Return the response
    return response

if __name__ == '__main__':
    # Use a production-ready WSGI server like Gunicorn or uWSGI in production
    # Ensure that the server is configured to use HTTPS
    # Set appropriate request size limits, timeouts, and logging configurations
    app.run(debug=False)  # It's important to set debug=False for production environments

