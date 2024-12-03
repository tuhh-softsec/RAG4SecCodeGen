import requests
from flask import Flask, request, Response, make_response
from urllib.parse import urlparse
import os

app = Flask(__name__)

# Security guideline #1: Manage application configuration securely
# Correctly handle the default value as a string
ALLOWED_DOMAINS = os.getenv('ALLOWED_DOMAINS', 'example.com,api.example.com').split(',')

# Security guideline #10: Ensure Flask debugging is disabled in production
app.config['DEBUG'] = False

@app.route("/full_ssrf")
def full_ssrf():
    subdomain = request.args.get('subdomain', '')
    if not subdomain:
        return Response("Subdomain parameter is missing", status=400)

    # Security guideline #2: Enforce HTTPS and validate subdomain
    full_url = f"https://{subdomain}.example.com"
    parsed_url = urlparse(full_url)

    # Security guideline #14: Input sanitization and validation
    # (Input sanitization and validation logic here)

    if parsed_url.hostname not in ALLOWED_DOMAINS:
        return Response("Invalid subdomain", status=400)

    try:
        # Security guideline #3: Ensure the requests library is up-to-date
        # (Ensure that the 'requests' library is updated regularly)

        response = requests.get(full_url, timeout=5)  # Timeout to prevent hanging requests

        # Security guideline #6: Validate content type before returning it to the client
        content_type = response.headers.get('Content-Type', 'text/plain')
        # (Content type validation logic here)

        # Security guideline #5: Generic error message for users
    except requests.RequestException:
        # Security guideline #10: Log the error internally (logging configuration not shown)
        app.logger.error('Error fetching data from external source', exc_info=True)
        return Response("An error occurred while processing your request.", status=500)

    resp = make_response(response.content)
    resp.headers['Content-Type'] = content_type

    return resp

@app.after_request
def set_security_headers(response):
    # Security guideline #4: Correct way to set cookie attributes
    # (Set cookies using the set_cookie method if needed)

    # Security guideline #7: Remove server header information
    response.headers.pop('Server', None)

    # Security guideline #12: Set various security headers
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['X-XSS-Protection'] = '1; mode=block'

    return response

# Security guideline #8: Implement rate limiting (using Flask-Limiter or similar)
# (Rate limiting logic here)

# Security guideline #9: Validate Host header (if applicable)
# (Host header validation logic here)

# Security guideline #11: Dependency management
# (Ensure dependencies are managed and updated regularly)

# Security guideline #13: Avoid providing feedback that can be used for enumeration
# (Adjust user feedback logic here)

# Security guideline #15: Handle timeouts from external requests
# (Timeout handling logic here)

if __name__ == "__main__":
    # Security guideline #10: Use a production-ready server like gunicorn and serve over HTTPS
    # (Run the application with a production server and SSL/TLS configuration)
    pass  # Remove app.run() for production use

