import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Securely load the secret key from an environment variable or a secure key management system
SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable not set")

# Define trusted issuer and audience values
TRUSTED_ISSUER = 'your_trusted_issuer'
TRUSTED_AUDIENCE = 'your_trusted_audience'

# Define a fixed algorithm to use for decoding the JWT
FIXED_ALGORITHM = 'HS256'

def verifyJWTToken(token):
    '''
    Decode the JWT token with the given key and return it.
    
    :param token: The JWT token to be verified and decoded.
    :return: The decoded token if verification is successful, None otherwise.
    '''
    try:
        # Decode the token with the given key and additional validation checks
        decoded_token = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[FIXED_ALGORITHM],
            issuer=TRUSTED_ISSUER,
            audience=TRUSTED_AUDIENCE
        )
        return decoded_token
    except ExpiredSignatureError:
        logger.error("Token has expired.")
        return None
    except InvalidTokenError as e:
        logger.error(f"Invalid token: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None

# Example usage:
# Replace 'your.jwt.token' with your actual JWT token
token = 'your.jwt.token'
decoded = verifyJWTToken(token)
if decoded:
    logger.info("Token verified and decoded: %s", decoded)
else:
    logger.info("Token could not be verified.")

# Ensure that the token is obtained from a secure and trusted source, such as an HTTPS-protected API endpoint or a secure cookie.
# Ensure that JWTs are always transmitted over secure channels (e.g., HTTPS) to prevent man-in-the-middle attacks.
# Implement key rotation and secure token storage practices.
# Consider token renewal mechanisms for short-lived JWTs and use nonce or JWT ID (JTI) to prevent replay attacks.
# Implement scope and permission checks as part of the token verification process.

