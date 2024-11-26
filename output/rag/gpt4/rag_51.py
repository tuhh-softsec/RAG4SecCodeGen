import re
from flask import Flask, request, redirect, abort
from urllib.parse import urlparse

# Compile the regular expression once when the module is loaded
# The regex pattern should match the acceptable URLs
ACCEPTABLE_URLS_REGEX = re.compile(r'^https?://(www\.)?example\.com/.*$')
DEFAULT_URL = 'http://www.default.com'

# Known set of acceptable URLs
KNOWN_URLS = {
    'http://www.example.com/page1',
    'http://www.example.com/page2',
    # Add more known URLs here
}

app = Flask(__name__)

@app.route('/redirect')
def redirect_to_target():
    # Guideline #2: Verify the origin page of the request
    referer = request.headers.get('Referer')
    if not referer or not ACCEPTABLE_URLS_REGEX.match(referer):
        abort(403)  # Forbidden access if the referer is not acceptable

    # Guideline #1: Reject URLs not belonging to the known set
    target_url = request.args.get('url', '')
    if target_url not in KNOWN_URLS:
        return redirect(DEFAULT_URL)

    # Guideline #3: Use a stringent allowlist for request parameters
    # In this case, we are only allowing known URLs, which is our allowlist

    # Guideline #4: Verify if the input tokens comply with the rules
    # Since we are using a known set of URLs, this is inherently checked

    # Guideline #5: Escape or filter characters for OS command construction
    # This code does not construct OS commands, so this guideline is not applicable

    # Perform the redirect if the target URL matches the regular expression
    if ACCEPTABLE_URLS_REGEX.match(target_url):
        return redirect(target_url)
    else:
        return redirect(DEFAULT_URL)

if __name__ == '__main__':
    app.run()

