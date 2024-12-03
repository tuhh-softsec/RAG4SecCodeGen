from datetime import timedelta
from flask import Flask, redirect, request, url_for, make_response
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Load secret key from environment variable or generate a random one
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_NAME'] = 'myapp_session'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(hours=1)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize Talisman for setting security headers
csp = {
    'default-src': '\'self\'',
    # Add other CSP policies as needed
}
Talisman(app, content_security_policy=csp)

# Initialize rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Define a list of allowed hosts for safer redirection
ALLOWED_HOSTS = ['www.example.com', 'example.com']

# Set up logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

def is_safe_url(target):
    """
    Determine if the URL is safe for redirects by checking against a list of allowed hosts.
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.hostname in ALLOWED_HOSTS

@app.route('/set_location_header')
def set_location_header():
    next_url = request.args.get('next', '')
    if next_url and is_safe_url(next_url):
        response = redirect(next_url)
        app.logger.info(f"Redirect to {next_url}")  # Log successful redirection
        return response
    else:
        app.logger.warning(f"Unsafe redirect attempt to {next_url}")  # Log failed redirection attempts
        return redirect(url_for('index'))

@app.route('/')
def index():
    return 'Welcome to the homepage!'

@app.errorhandler(404)
def page_not_found(e):
    # Log the error and provide a custom error message
    app.logger.error(f"Page not found: {request.url}")
    return 'This page does not exist', 404

@app.errorhandler(500)
def internal_server_error(e):
    # Log the error and provide a custom error message
    app.logger.error(f"Internal server error: {e}")
    return 'Internal server error', 500

# Production deployment should use a production-ready WSGI server like Gunicorn or uWSGI
# and should be behind a reverse proxy like Nginx or Apache.

# Ensure to keep Flask-WTF, Flask-Talisman, and other dependencies up to date
# Implement automated processes for dependency management and security patching

# The code should be reviewed and tested to ensure that all security measures are properly implemented
# before moving to a production environment.

