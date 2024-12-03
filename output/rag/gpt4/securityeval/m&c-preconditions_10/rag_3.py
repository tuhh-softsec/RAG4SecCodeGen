from flask import Flask, request, make_response, escape, session
import html

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Ensure debugging is disabled
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# Implement a simple rate limiting mechanism
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Set up rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def rate_limit_exceeded():
    return "You have exceeded your request limit", 429

limiter.register_error_handler(rate_limit_exceeded)

@app.route("/profile")
@limiter.limit("10 per minute")  # Guideline #1: Limit the number of requests
def profile():
    '''
    Get the username from the request, make a response with it and return it
    '''
    # Guideline #9: Do not accept untrusted data as input from a web request
    # Guideline #7: Validate the data in the request
    username = request.args.get('username', '')
    if not username.isalnum():
        return "Invalid username", 400

    # Guideline #4: Escape the input before writing user input to the page
    safe_username = html.escape(username)

    # Guideline #3: Do not reflect data directly back in the response
    response = make_response(f"Profile page for {safe_username}")

    # Guideline #5: Set the session cookie to HttpOnly
    session['username'] = safe_username
    response.set_cookie('session', session['username'], httponly=True)

    # Guideline #6: Specify encoding in the HTTP header
    response.headers['Content-Type'] = 'text/html; charset=utf-8'

    return response

if __name__ == "__main__":
    app.run()

