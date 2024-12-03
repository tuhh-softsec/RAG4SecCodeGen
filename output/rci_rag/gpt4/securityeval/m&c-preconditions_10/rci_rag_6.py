import os
from flask import Flask, redirect, request, abort, session, render_template
from flask_wtf.csrf import CSRFProtect
from urllib.parse import urlparse, urljoin
from itsdangerous import URLSafeTimedSerializer
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask.logging import create_logger

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')  # Fallback to a default key if not set
app.config['DEBUG'] = False  # Ensure that Flask application is run with debugging disabled

# Ensure the SECRET_KEY is not the default or empty
if app.config['SECRET_KEY'] == 'default-secret-key' or not app.config['SECRET_KEY']:
    raise ValueError("The SECRET_KEY environment variable must be set to a non-default, non-empty value.")

# Enable CSRF protection
csrf = CSRFProtect(app)

# Enforce HTTPS and set a basic CSP
csp = {
    'default-src': '\'self\''
}
talisman = Talisman(app, content_security_policy=csp)

# Rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Logging
logger = create_logger(app)

# Load safe URLs from a configuration file or environment variable
SAFE_URLS = os.environ.get('SAFE_URLS', 'http://example.com,https://example.com').split(',')

# Serializer for generating and verifying tokens
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc and \
           test_url.path and test_url.query

@app.route('/redirect', methods=['GET', 'POST'])
@limiter.limit("10 per minute")  # Apply rate limiting to sensitive endpoint
def redirectToTarget():
    if request.method == 'POST':
        # Confirm the dangerous action
        target = session.pop('target_url', None)  # Use pop to remove the target URL from the session
        if not target or not is_safe_url(target):
            abort(400, description="Invalid or missing target URL.")
        return redirect(target)

    target = request.args.get('url', None)
    if not target or not is_safe_url(target):
        abort(400, description="Missing or invalid target URL parameter.")

    # Store the target URL in the session for the confirmation step
    session['target_url'] = target

    # Render a confirmation page
    return render_template('confirm_redirect.html', target_url=target)

@app.errorhandler(404)
def page_not_found(e):
    # Custom error handling for 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    # Custom error handling for 500
    return render_template('500.html'), 500

# Remove server header information
@app.after_request
def remove_server_header(response):
    response.headers['Server'] = 'SecureServer'
    return response

if __name__ == '__main__':
    # Check for required environment variables
    if not os.environ.get('SECRET_KEY'):
        raise RuntimeError("SECRET_KEY environment variable is not set.")
    app.run()

