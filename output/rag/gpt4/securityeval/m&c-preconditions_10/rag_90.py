from flask import request, redirect, Flask, abort
from urllib.parse import urlparse, urljoin
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Ensure Flask app is run with debugging disabled

# List of known and allowed hosts for redirection
ALLOWED_HOSTS = ['www.example.com', 'sub.example.com']

@app.route('/flask_redirect')
def flask_redirect():
    '''
    Get the url from the request and redirect to it
    '''
    # Guideline #4: Do not accept untrusted data as input from a web request
    # Guideline #7: Validate the data in the request
    url = request.args.get('url', '')
    if not url:
        abort(400, description="Missing URL parameter")

    # Guideline #2: Parse a URL before performing a check on its host value
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        abort(400, description="Invalid URL format")

    # Guideline #3: Reject URLs not belonging to the known set of URLs
    if parsed_url.netloc not in ALLOWED_HOSTS:
        abort(400, description="URL host is not allowed")

    # Guideline #1: Handle arbitrary subdomain sequences in a URL correctly
    # This is handled by checking the netloc against the ALLOWED_HOSTS list

    # Guideline #8: Use stringent allowlist for character sets in dynamic webpages
    # This is handled by validating the URL and only allowing known hosts

    # Guideline #9: Do not reflect data directly back in the HTTP response
    # The redirection URL is validated and not directly reflected back

    # Create a secure redirect URL, ensuring it's relative to the host
    secure_url = urljoin(request.host_url, secure_filename(parsed_url.path))
    if secure_url != url:
        abort(400, description="Invalid URL redirection")

    # Perform the redirect
    return redirect(secure_url)

# Guideline #5: Set the session cookie to HttpOnly
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Guideline #6: Specify encoding in the HTTP header
@app.after_request
def set_response_headers(response):
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

if __name__ == '__main__':
    app.run()

