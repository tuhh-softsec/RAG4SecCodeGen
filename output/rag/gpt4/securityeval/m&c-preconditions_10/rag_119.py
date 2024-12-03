import requests
from flask import Flask, request, jsonify, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a real secret key
app.config['DEBUG'] = False  # Ensure debug mode is off in production

# Set up rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Decorator to check if the user is authorized
def require_authorization(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Implement your authorization logic here
        # For example, check if the user has a valid token/session
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

# Apply the rate limiter to the route
@app.route("/user")
@limiter.limit("5 per minute")  # Adjust the rate limit as needed
@require_authorization
def retrieve_info():
    '''
    Get the user_id from the request,
    then retrieve the user info from GitHub using the GitHub's API,
    and return the response
    '''
    user_id = request.args.get('user_id', type=str)
    
    # Validate the user_id to ensure it's alphanumeric (allowlist)
    if not user_id.isalnum():
        return jsonify({"error": "Invalid user_id"}), 400

    # Construct the GitHub API URL
    url = f"https://api.github.com/users/{user_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch user info"}), 500

    # Return the JSON response from GitHub
    return jsonify(response.json()), response.status_code

# Set the session cookie to HttpOnly
@app.after_request
def apply_http_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Set-Cookie"] = "HttpOnly; Secure"
    return response

if __name__ == "__main__":
    app.run()

