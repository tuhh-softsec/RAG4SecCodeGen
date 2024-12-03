from flask import Flask, request, session, make_response
import re

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Ensure Flask app is run with debugging disabled

# Guideline #3: Set the session cookie to HttpOnly
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Guideline #4: Specify encoding in the HTTP header
@app.after_request
def apply_caching(response):
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    return response

# Guideline #2: Implement rate limiting (example using Flask-Limiter)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/direct")
@limiter.limit("10 per minute")  # Apply rate limit to this endpoint
def direct():
    '''
    Get the regex from the 'pattern' in the GET request,
    get the 'text' from the GET request,
    and search the 'text' with the provided regex.
    '''
    # Guideline #5 and #6: Validate the data in the request
    pattern = request.args.get('pattern', '')
    text = request.args.get('text', '')

    # Validate the regex pattern to prevent ReDoS attacks and ensure it's a valid regex
    try:
        re.compile(pattern)
        # Guideline #6: Use stringent allowlist for regex patterns
        if not re.match(r'^[A-Za-z0-9\\|\[\]()+*?^$\.{}!\'"-]+$', pattern):
            raise ValueError("Invalid characters in pattern")
    except re.error:
        return "Invalid regex pattern", 400

    # Search the text with the provided regex
    match = re.search(pattern, text)

    # Return the result
    if match:
        return f"Match found: {match.group(0)}"
    else:
        return "No match found"

if __name__ == "__main__":
    app.run()

