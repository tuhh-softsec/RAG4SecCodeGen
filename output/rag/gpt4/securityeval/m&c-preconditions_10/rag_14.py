from flask import Flask, request, make_response, abort, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Ensure Flask app is run with debugging disabled

# Guideline #1: Implement rate limiting to prevent users from making too many requests
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per minute"]  # Adjust the rate limit as needed
)

# Guideline #4: Define an allowlist for input validation
ALLOWED_NAME_PATTERN = re.compile(r'^[a-zA-Z\s]{1,50}$')

@app.route('/showName')
@limiter.limit("5 per minute")  # Guideline #1: Limit the number of requests per minute
def name():
    '''
    Get "name" from the request, validate it,
    make a response with it, and return the response object
    '''
    # Guideline #7 and #8: Validate the data in the request
    name = request.args.get('name', '')
    if not ALLOWED_NAME_PATTERN.match(name):
        abort(400, description="Invalid name provided.")

    # Guideline #9: Escape special characters before writing the HTTP parameter back to the page
    safe_name = html.escape(name)

    # Guideline #2: Do not reflect data directly back in the response
    # Instead, use a safe, escaped version of the data
    response = make_response(jsonify(message=f"Hello, {safe_name}"))

    # Guideline #5: Set the session cookie to HttpOnly
    response.set_cookie('session', 'value', httponly=True)

    # Guideline #6: Specify encoding in the HTTP header
    response.headers['Content-Type'] = 'application/json; charset=utf-8'

    return response

if __name__ == '__main__':
    app.run()

