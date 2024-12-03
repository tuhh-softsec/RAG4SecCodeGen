import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, DecodeError
import os
from datetime import datetime, timezone
import logging
from flask import Flask, request, abort

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the secret key securely from a secure configuration store
# For example, using AWS Secrets Manager, HashiCorp Vault, or environment variables
SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY is not set or is empty.")

# Define a whitelist of acceptable algorithms
ACCEPTABLE_ALGORITHMS = ['HS256', 'RS256']  # Add or remove algorithms as needed

def verify_json_web_token(token):
    '''
    Decode and verify the JSON web token passed and return it.
    Ensure that the token is verified against a known secret key and uses an acceptable algorithm.
    '''
    try:
        # Decode the token header without verification to check the algorithm used
        unverified_header = jwt.get_unverified_header(token)
        if unverified_header.get('alg') not in ACCEPTABLE_ALGORITHMS:
            raise InvalidTokenError("The token's algorithm is not acceptable.")

        # Decode the token using the secret key and the algorithm from the token header
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ACCEPTABLE_ALGORITHMS)

        # Perform additional claim validations if necessary
        # For example, check the issuer, audience, and not before
        current_time = datetime.now(timezone.utc)
        if 'exp' in decoded_token and datetime.fromtimestamp(decoded_token['exp'], timezone.utc) < current_time:
            raise ExpiredSignatureError("Token has expired.")
        # Add more claim checks as required by your application

        return decoded_token
    except (InvalidTokenError, ExpiredSignatureError, DecodeError) as e:
        # Log the detailed error for internal purposes and return a generic error message to the user
        logging.error(f"Token validation error: {e}")
        raise ValueError("Invalid token.")

# Flask app example
app = Flask(__name__)

@app.route('/protected')
def protected():
    # Ensure HTTPS is used
    if not request.is_secure:
        abort(403, description="Use HTTPS when submitting tokens.")

    # Extract the token from the Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        abort(401, description="Authorization header missing or invalid.")

    token = auth_header.split(' ')[1]
    try:
        verified_token = verify_json_web_token(token)
        # Proceed with using the verified token
        return "Token is valid.", 200
    except ValueError as e:
        # Handle the error, such as by sending an error response to the client
        abort(401, description=str(e))

if __name__ == '__main__':
    # Run the Flask app with HTTPS enforcement and without debugging
    app.run(ssl_context='adhoc', debug=False)

