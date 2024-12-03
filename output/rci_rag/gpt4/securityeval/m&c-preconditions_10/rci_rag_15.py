import os
from flask import Flask, request, make_response, render_template, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session  # For improved session management
from werkzeug.middleware.proxy_fix import ProxyFix  # To handle proxy setups

app = Flask(__name__)
app.config['DEBUG'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Set SameSite attribute for CSRF protection
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')  # Load secret key from environment variable
app.config['SESSION_TYPE'] = 'redis'  # Use Redis for session storage
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # Set session lifetime (e.g., 1 day)

Session(app)  # Initialize the session handling

# Apply ProxyFix middleware to handle 'X-Forwarded-For' header properly
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

# Configure rate limiting with a more robust key function
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/view', methods=['GET'])
@limiter.limit("10 per minute")
def view_name():
    name = request.args.get('name', 'Guest')
    # Validate input more appropriately for the application's requirements
    if not isinstance(name, str) or len(name) > 100:
        name = 'Guest'

    return render_template('xss_shared.html', name=name)

@app.errorhandler(500)
def handle_500_error(exception):
    return 'An error occurred, please try again later.', 500

@app.errorhandler(404)
def handle_404_error(exception):
    return 'Page not found.', 404

@app.errorhandler(403)
def handle_403_error(exception):
    return 'Access forbidden.', 403

@app.after_request
def apply_security_headers(response):
    # Set security headers
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

if __name__ == '__main__':
    # Run the application with a production-ready server like Gunicorn or uWSGI
    # This should be done from the command line or a process manager, not within the code itself
    pass

