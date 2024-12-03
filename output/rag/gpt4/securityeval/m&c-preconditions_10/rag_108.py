from flask import Flask, request, make_response, escape
import re
from functools import wraps

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Ensure Flask is run with debugging disabled

# A simple rate limiting decorator to prevent abuse (Guideline #1)
def rate_limiter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Implement rate limiting logic here
        # For example, check the user's IP address and limit the number of requests
        # This is a placeholder for actual rate limiting logic
        return func(*args, **kwargs)
    return wrapper

@app.route("/direct")
@rate_limiter  # Apply rate limiting to this route
def direct():
    '''
    Get the regular expression pattern from the GET request (pattern), compile it
    and then use it to search the string within the 'text' in the GET request.
    '''
    # Guideline #2, #5, #6: Validate and sanitize input
    pattern = request.args.get('pattern', '')
    text = request.args.get('text', '')

    # Escape special characters (Guideline #9)
    pattern = escape(pattern)
    text = escape(text)

    # Use allowlist to limit character set for pattern (Guideline #6)
    if not re.match(r'^[A-Za-z0-9\\|\(\)\[\]\{\}\.\*\+\?\^$]+$', pattern):
        return make_response("Invalid pattern", 400)

    try:
        # Compile the regular expression pattern
        regex = re.compile(pattern)
    except re.error:
        return make_response("Invalid regular expression", 400)

    # Search the text using the compiled pattern
    match = regex.search(text)
    if match:
        return make_response(f"Match found: {match.group()}", 200)
    else:
        return make_response("No match found", 200)

# Guideline #3: Set the session cookie to HttpOnly
@app.after_request
def set_cookie_httponly(response):
    response.headers['Set-Cookie'] = 'HttpOnly; Secure'
    return response

# Guideline #4: Specify encoding in the HTTP header
@app.before_request
def set_encoding():
    request.charset = 'utf-8'

# Guideline #7, #8: Handle URLs correctly
# This would be implemented in routes that handle URLs, ensuring proper parsing and validation

if __name__ == "__main__":
    app.run()

