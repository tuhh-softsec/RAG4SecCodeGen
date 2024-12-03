from flask import Flask, request, redirect, abort, session, make_response
from urllib.parse import urlparse, urljoin
from datetime import timedelta
from functools import wraps
import os

app = Flask(__name__)

# Guideline #1: Set a persistent secret key for securely signing the session cookie
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

# Guideline #2: Enforce HTTPS
@app.before_request
def enforce_https():
    if not request.is_secure and app.env != 'development':
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

# Guideline #5: Set a Content Security Policy (CSP)
@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

# Guideline #6: Set headers for XSS Protection
@app.after_request
def set_xss_protection_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# Guideline #12: Set other security-related headers
@app.after_request
def set_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Permissions-Policy'] = "geolocation 'self'"
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response

# Guideline #13: Set session expiration
app.permanent_session_lifetime = timedelta(minutes=30)

# Known set of URLs for redirection
ALLOWED_HOSTS = {'example.com', 'sub.example.com'}

def is_safe_url(target):
    """
    Check if the URL is safe for redirects.
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           test_url.hostname in ALLOWED_HOSTS

def validate_url(f):
    """
    Decorator to validate URLs before processing the request.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        next_url = request.args.get('next_url', '')
        if not is_safe_url(next_url):
            abort(400)  # Bad request if the URL is not safe
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@validate_url
def redirect_to_next():
    """
    Redirect the user to the next_url specified on the GET request.
    """
    next_url = request.args.get('next_url', '')
    # Guideline #11: Validate and sanitize all user inputs
    # Here we assume that next_url has been validated by is_safe_url
    return redirect(next_url)

if __name__ == '__main__':
    # Run the app
    app.run(ssl_context='adhoc')  # Use ad-hoc SSL for demonstration purposes

