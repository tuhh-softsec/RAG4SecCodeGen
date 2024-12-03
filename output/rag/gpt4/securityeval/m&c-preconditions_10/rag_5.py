from flask import Flask, redirect, request, abort, make_response
from urllib.parse import urlparse
import re
import os

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Ensure Flask is run with debugging disabled

# List of known and allowed URLs for redirection
ALLOWED_URLS = ['https://example.com', 'https://sub.example.com']

# Regular expression pattern to validate URLs
URL_PATTERN = re.compile(
    r'^(?:http|https)://'  # http:// or https://
    r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'  # domain
    r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)'  # domain extension
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

@app.route('/redirect', methods=['GET'])
def redirectToTarget():
    '''
    Get target URL from request,
    use a regular expression to check if it is a valid target,
    then redirect to the target URL
    '''
    # Guideline #5: Verify the origin page of the request by checking the HTTP Referer header
    referer = request.headers.get('Referer')
    if not referer or not any(referer.startswith(allowed_url) for allowed_url in ALLOWED_URLS):
        abort(403)  # Forbidden access if the referer is not from the allowed URLs

    # Get target URL from request
    target_url = request.args.get('url', '')

    # Guideline #3: Parse a URL before performing a check on its host value
    parsed_url = urlparse(target_url)

    # Guideline #1: Reject URLs not belonging to the known set of URLs
    if not any(parsed_url.netloc.endswith(allowed_url) for allowed_url in ALLOWED_URLS):
        abort(400)  # Bad request if the URL is not allowed

    # Guideline #2: Handle arbitrary subdomain sequences in a URL correctly
    # This is implicitly handled by checking the netloc with known allowed URLs

    # Check if the URL matches the regular expression pattern
    if not URL_PATTERN.match(target_url):
        abort(400)  # Bad request if the URL does not match the pattern

    # Guideline #8: Prevent XSS attacks by escaping the URL
    safe_target_url = re.escape(target_url)

    # Redirect to the target URL
    return redirect(safe_target_url)

if __name__ == '__main__':
    # Generate a cryptographically strong pseudorandom value as a secret key
    app.secret_key = os.urandom(24)  # Guideline #7
    app.run()

