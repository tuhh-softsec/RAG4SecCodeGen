import base64
from flask import Flask, request, make_response, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Ensure Flask app is run with debugging disabled.

# Apply rate limiting to prevent abuse (Guideline #1)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per minute"]
)

# Helper function to check authorization (Guideline #3)
def check_authorization():
    # Implement your authorization check here
    # For example, check for a valid API token in the request headers
    auth_token = request.headers.get('Authorization')
    if not auth_token or auth_token != "YourExpectedToken":
        return False
    return True

def require_authorization(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not check_authorization():
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function

# Helper function to validate and decode base64 input (Guideline #7, #8, #9)
def decode_base64(input_str):
    # Validate that input is base64 encoded
    try:
        base64_bytes = input_str.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
        return message
    except (ValueError, UnicodeDecodeError):
        return None

@app.route("/execute", methods=['POST'])
@limiter.limit("5 per minute")  # Apply a more specific rate limit to this endpoint if needed
@require_authorization  # Ensure the user is authorized (Guideline #3)
def code_execution():
    # Get "first_name" from the post request object (Guideline #7)
    first_name_encoded = request.json.get('first_name')
    if not first_name_encoded:
        return jsonify({"error": "Missing 'first_name' parameter"}), 400

    # Decode the string using base64 (Guideline #7, #8, #9)
    first_name = decode_base64(first_name_encoded)
    if not first_name:
        return jsonify({"error": "Invalid 'first_name' parameter"}), 400

    # Call the setname function with the decoded first_name as argument
    # Assuming setname is a function you have defined elsewhere
    setname(first_name)

    # Create a response object (Guideline #2, #4, #5, #6)
    response = make_response(jsonify({"message": "Name set successfully"}), 200)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'  # Guideline #6
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.set_cookie('session', 'value', httponly=True)  # Guideline #5

    return response

# Dummy function to represent setting the name
def setname(name):
    # Implement the logic to set the name here
    pass

if __name__ == "__main__":
    app.run()

