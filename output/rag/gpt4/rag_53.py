from flask import Flask, request, redirect, url_for
import re
from urllib.parse import urlparse, urljoin
from werkzeug.utils import escape

app = Flask(__name__)

# Regular expression pattern to match the required string format
# Starts with one or more alphanumeric characters or hyphens followed by a period
pattern = re.compile(r'^[\w-]+\.')

@app.route('/redirect')
def redirect_target():
    # Get the target query parameter
    target = request.args.get('target', '')

    # Guideline #1: Verify the origin page of the request
    referer = request.headers.get('Referer')
    if not referer or not is_valid_referer(referer):
        return redirect(url_for('index'))

    # Guideline #2: Restrict the filename to have only a single "." character and exclude directory separators
    if not is_valid_path(target):
        return redirect(url_for('index'))

    # Guideline #3: Escape or filter all characters that do not pass an extremely strict allowlist
    target = escape(target)

    # Check if the target matches the regular expression
    if pattern.match(target):
        # Redirect to the target if it matches the pattern
        return redirect(target)
    else:
        # Redirect to the root of the site if it does not match
        return redirect(url_for('index'))

def is_valid_referer(referer):
    # Check if the referer is from the same site
    server_host = urlparse(request.host_url).hostname
    referer_host = urlparse(referer).hostname
    return server_host == referer_host

def is_valid_path(path):
    # Check if the path has only a single "." character and no directory separators
    return path.count('.') == 1 and '/' not in path and '\\' not in path

@app.route('/')
def index():
    # Guideline #4: Encode all non-alphanumeric characters for web page output
    # This is handled by Flask's template rendering which auto-escapes variables
    return 'Welcome to the site!'

if __name__ == '__main__':
    app.run()

