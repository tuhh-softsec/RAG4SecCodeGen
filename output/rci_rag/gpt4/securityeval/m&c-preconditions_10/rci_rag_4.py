import base64
import json
import logging
from flask import Flask, request, abort, make_response, jsonify
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

app = Flask(__name__)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize Talisman for HTTPS and security headers
Talisman(app, content_security_policy=None)  # CSP is set to None for demonstration; define a strict CSP for production

# Initialize CORS with a strict policy for production
CORS(app, resources={r"/api/*": {"origins": "https://yourdomain.com"}})

# Initialize Limiter for rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.errorhandler(500)
def handle_exception(e):
    logging.error(f"An error occurred: {str(e)}")  # Log the exception
    return jsonify(error=str(e)), 500

@app.route("/profile")
@limiter.limit("10 per minute")  # Apply rate limiting to the profile route
def profile():
    if 'data' not in request.args:
        abort(400, description="Bad Request: Missing 'data' parameter.")

    raw_data = request.args.get('data')

    if not is_base64(raw_data):
        abort(400, description="Bad Request: Invalid 'data' parameter.")

    try:
        decoded_data = base64.b64decode(raw_data)
        deserialized_data = safe_deserialize(decoded_data)
    except Exception as e:
        handle_exception(e)
        abort(400, description="Bad Request: Unable to process the provided data.")

    # Ensure that only non-sensitive data is returned
    response = jsonify(profile_data=deserialized_data)
    return response

def is_base64(s):
    try:
        base64.b64decode(s)
        return True
    except base64.binascii.Error:
        return False

def safe_deserialize(data):
    # Use json.loads for secure deserialization
    return json.loads(data)

if __name__ == "__main__":
    # For production, replace 'adhoc' with a tuple containing the cert and key files
    app.run(ssl_context=('cert.pem', 'key.pem'))

