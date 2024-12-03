import python_jwt as jwt
import jwcrypto.jwk as jwk
import jwcrypto.jwt as jwttoken
from jwcrypto.common import json_encode, json_decode
import hashlib
import os

# Load your secret key from a secure place. This could be an environment variable,
# a file with restricted permissions, or a secure key management system.
# For this example, we'll assume an environment variable.
SECRET_KEY_ENV_VAR = 'JWT_SECRET_KEY'
SECRET_KEY = os.environ.get(SECRET_KEY_ENV_VAR)

if not SECRET_KEY:
    raise Exception("Secret key for JWT verification is not set.")

# Convert the secret key to a JWK object
key = jwk.JWK.from_json(json_encode({"k": hashlib.sha256(SECRET_KEY.encode('utf-8')).hexdigest(), "kty": "oct"}))

def verifyJWTToken(jwt_token):
    '''
    Verify the JWT Token and return it.
    '''
    # Verify if the input token is a valid JWT token
    if not isinstance(jwt_token, str):
        raise ValueError("Invalid token: Token must be a string.")

    try:
        # Decode and verify the JWT token
        token = jwttoken.JWT(key=key, jwt=jwt_token)
        token.verify()
        claims = json_decode(token.claims)
        return claims
    except (jwt.JWTError, jwt.JWTExpired, jwt.JWTClaimsError) as e:
        # Handle token verification errors (e.g., signature failure, expired token)
        raise ValueError(f"Invalid token: {str(e)}")

# Example usage:
# try:
#     verified_claims = verifyJWTToken('<your_jwt_token_here>')
#     print(verified_claims)
# except ValueError as e:
#     print(e)

# Ensure Flask application is run with debugging disabled
# if __name__ == "__main__":
#     from flask import Flask
#     app = Flask(__name__)
#     app.debug = False  # Disable debugging
#     app.run()

