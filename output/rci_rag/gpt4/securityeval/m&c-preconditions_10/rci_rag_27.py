from flask import Flask, request, Response, abort, session, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
import os

app = Flask(__name__)

# Configuration for secure session management
app.config['SESSION_TYPE'] = 'redis'  # Use Redis for session storage
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent client-side scripts from accessing the cookie
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')  # Read the secret key from an environment variable

# Initialize Flask-Session
Session(app)

# Initialize Flask-Limiter for rate limiting based on client IP
limiter = Limiter(
    app,
    key_func=get_remote_address,  # Consider using a function that accounts for 'X-Forwarded-For' if behind a proxy
    default_limits=["100 per day", "10 per hour"]
)

# Ensure that Flask application is run with debugging disabled
app.config['DEBUG'] = False

@app.before_request
def before_request():
    # Enforce HTTPS in production by redirecting HTTP to HTTPS
    if not request.is_secure and app.env == 'production':
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

@app.route('/')
@limiter.limit("5 per minute")  # Apply rate limiting to this endpoint
def route():
    '''
    Get the content_type parameter from the request,
    create a response with the content_type and send it as a response.
    '''
    # Get the content_type parameter from the request
    content_type = request.args.get('content_type', 'text/plain')
    
    # Use an allowlist to limit the character set for content_type
    allowed_content_types = ['text/plain', 'text/html', 'application/json']
    if content_type not in allowed_content_types:
        abort(400, description="Invalid content type.")
    
    # Create a response with the specified content_type
    response = Response("Your content type is: {}".format(content_type), mimetype=content_type)
    
    # Set a session value
    session['value'] = 'example'
    
    return response

@app.errorhandler(429)
def ratelimit_handler(e):
    return Response("You have exceeded your request limit.", status=429)

@app.errorhandler(400)
def bad_request_handler(e):
    # Log the error details server-side
    app.logger.error(f"Bad request: {e.description}")
    # Present a generic error message to the client
    return Response("Bad request. Please check your input and try again.", status=400)

@app.errorhandler(500)
def internal_server_error_handler(e):
    # Log the error details server-side
    app.logger.error(f"Internal server error: {e.description}")
    # Present a generic error message to the client
    return Response("An internal server error occurred. Please try again later.", status=500)

if __name__ == '__main__':
    # Run the application with SSL in production using a certificate from a trusted CA
    if app.env == 'production':
        app.run(ssl_context=('path/to/cert.pem', 'path/to/key.pem'))
    else:
        app.run()

