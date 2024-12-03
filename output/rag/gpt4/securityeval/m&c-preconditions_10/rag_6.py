from flask import Flask, redirect, request, abort, make_response
from urllib.parse import urlparse
import secrets

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Disable Flask debugging

# Known set of allowed domains
ALLOWED_DOMAINS = {'example.com', 'sub.example.com'}

@app.route('/redirect')
def redirectToTarget():
    '''
    Get target URL from request, check if it contains a valid domain, and 
    then redirect to the target URL
    '''
    # Guideline #1: Reject URLs not belonging to the known set of URLs
    target_url = request.args.get('url', '')
    if not target_url:
        abort(400, description="Missing URL parameter")

    # Guideline #3: Parse the URL before checking its host value
    parsed_url = urlparse(target_url)
    domain = parsed_url.netloc

    # Handle arbitrary subdomain sequences correctly (Guideline #2)
    if any(domain == allowed_domain or domain.endswith('.' + allowed_domain) for allowed_domain in ALLOWED_DOMAINS):
        # Guideline #5: Verify the origin page of the request
        referer = request.headers.get('Referer')
        if referer:
            parsed_referer = urlparse(referer)
            if parsed_referer.netloc not in ALLOWED_DOMAINS:
                abort(403, description="Invalid referer")

        # Guideline #7: Verify user intent (e.g., using a token or user confirmation)
        # This example assumes a token-based approach
        token = request.args.get('token', '')
        if not token or not validate_token(token):
            abort(403, description="Invalid or missing token")

        # Guideline #8: Prevent XSS attacks by ensuring that the redirect URL is safe
        # Flask's `redirect` function is safe against XSS as it escapes special characters

        # Perform the redirect
        return redirect(target_url)
    else:
        abort(403, description="Invalid domain")

def validate_token(token):
    # Implement token validation logic here
    # For example, check if the token exists in the database and is valid for the user
    return True

@app.after_request
def add_security_headers(response):
    # Guideline #9: Use vetted libraries or frameworks that do not allow CSRF
    # Flask has built-in protection against CSRF if you use Flask-WTF with CSRF protection enabled

    # Add additional security headers to response
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

# Guideline #6: Generate cryptographically strong pseudorandom value as cookie
@app.before_request
def before_request():
    if 'csrf_token' not in request.cookies:
        response = make_response()
        csrf_token = secrets.token_urlsafe(64)
        response.set_cookie('csrf_token', csrf_token)
        return response

if __name__ == '__main__':
    app.run()

