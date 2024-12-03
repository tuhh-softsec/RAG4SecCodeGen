from flask import Flask, request, render_template, make_response, session, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import re
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# Configure Talisman for HTTPS and CSP
csp = {
    'default-src': [
        '\'self\'',
        'https://trusted.cdn.com',
    ]
}
Talisman(app, content_security_policy=csp)

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Configure logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

@app.route("/renderHtml")
@limiter.limit("10 per minute")  # Rate limit for this endpoint
def renderHTML():
    '''
    Get "name" from request,
    render the name in html, make an HTTP response saying "Hello name",
    and return it
    '''
    # Get the "name" parameter from the query string and validate/sanitize it
    name = request.args.get("name", "World")  # Default to "World" if no name is provided
    # Perform necessary input validation and sanitization on the name
    if name:
        name = re.sub(r'[^\w\s]', '', name)  # Basic sanitization by removing non-alphanumeric characters

    # Use a static template file to avoid Server-Side Template Injection (SSTI)
    rendered_html = render_template('hello_template.html', name=name)

    # Make an HTTP response with the rendered HTML
    response = make_response(rendered_html)

    # Set security-related headers
    response.headers['Content-Type'] = 'text/html'
    response.headers['X-Content-Type-Options'] = 'nosniff'  # Prevent MIME type sniffing
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'  # Protect against clickjacking
    response.headers['Cache-Control'] = 'no-store'  # Prevent caching of sensitive data

    return response

@app.errorhandler(404)
def page_not_found(e):
    # Custom error handling for 404 errors
    app.logger.error(f'Page not found: {request.url}')
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    # Custom error handling for 500 errors
    app.logger.error(f'Internal server error: {e}')
    return render_template('500.html'), 500

if __name__ == "__main__":
    # Disable debug mode in production
    app.run(debug=False, ssl_context='adhoc')  # Use 'adhoc' for self-signed cert or provide cert paths

