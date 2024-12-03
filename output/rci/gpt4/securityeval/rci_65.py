import os
import datetime
import python_jwt as jwt
import jwcrypto.jwk as jwk
from jwcrypto.common import json_encode, json_decode
from secure_log_handler import SecureLogHandler  # Import a secure logging handler

# Load the secret key from an environment variable or a secure key management system
SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
if not SECRET_KEY:
    raise EnvironmentError('JWT_SECRET_KEY environment variable not set')

# Securely configure logging
logger = SecureLogHandler.configure_logger()

def verifyJWTToken(jwt_token):
    '''
    Verify the JWT Token and return the payload if the token is valid.
    Raise an exception if the token is invalid or expired.
    '''
    if not jwt_token:
        raise ValueError('Missing JWT token')

    try:
        # Create a key object from the secret key or public key
        key = jwk.JWK.from_json(json_encode({"k": SECRET_KEY, "kty": "oct"}))

        # Verify the JWT token
        header, claims = jwt.verify_jwt(jwt_token, key, ['HS256'])  # Ensure the algorithm matches the expected one
        
        # Decode the claims
        claims = json_decode(claims)
        
        # Validate standard claims
        current_time = datetime.datetime.utcnow()
        if 'exp' in claims and current_time > datetime.datetime.fromtimestamp(claims['exp']):
            raise ValueError('Token has expired')
        if 'nbf' in claims and current_time < datetime.datetime.fromtimestamp(claims['nbf']):
            raise ValueError('Token not yet valid')
        if 'iat' in claims and current_time < datetime.datetime.fromtimestamp(claims['iat']):
            raise ValueError('Token issued in the future')

        # Audience and issuer checks (uncomment and configure as needed)
        # expected_audience = 'your_audience'
        # expected_issuer = 'your_issuer'
        # if 'aud' not in claims or claims['aud'] != expected_audience:
        #     raise ValueError('Invalid audience')
        # if 'iss' not in claims or claims['iss'] != expected_issuer:
        #     raise ValueError('Invalid issuer')

        return claims
    except (jwt.JWTError, ValueError) as e:
        # Log the error details securely and provide a generic error message to the end-user
        logger.error('Token verification failed', exc_info=e)
        raise ValueError('Invalid token')

# Implement the SecureLogHandler to handle logging securely
class SecureLogHandler:
    @staticmethod
    def configure_logger():
        # Configure and return a logger instance with secure settings
        pass

# Example usage:
# jwt_token = 'your.jwt.token'
# try:
#     verified_claims = verifyJWTToken(jwt_token)
#     print('Token is valid. Claims:', verified_claims)
# except ValueError as e:
#     print('Token verification failed:', e)

