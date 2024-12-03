import jwt
import os
import logging
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, DecodeError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the secret key securely from an environment variable or a secure configuration management system
SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
if not SECRET_KEY:
    logger.error("JWT_SECRET_KEY environment variable is not set.")
    raise ValueError("Missing secret key for JWT decoding.")

# Define the expected issuer and audience
EXPECTED_ISSUER = 'your_expected_issuer'
EXPECTED_AUDIENCE = 'your_expected_audience'

# Retrieve the algorithm from a secure configuration
ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')

def verifyJsonWebToken(token):
    '''
    Decode the JSON web token passed and return it.
    If the token is invalid or expired, raise an exception.
    '''
    try:
        # Decode the token with the secret key and validate the issuer and audience
        decoded_token = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            issuer=EXPECTED_ISSUER,
            audience=EXPECTED_AUDIENCE
        )
        return decoded_token
    except ExpiredSignatureError:
        logger.warning("Token has expired.")
        raise
    except DecodeError:
        logger.warning("Token is invalid.")
        raise
    except InvalidTokenError as e:
        # Handle other InvalidTokenError exceptions
        logger.warning(f"Invalid Token: {e}")
        raise
    except Exception as e:
        # Handle unexpected exceptions
        logger.error(f"Unexpected error during token verification: {type(e).__name__}")
        raise

# Example usage:
# token = 'your.jwt.token'
# try:
#     verified_token = verifyJsonWebToken(token)
#     logger.info("Token verified successfully.")
# except Exception as e:
#     logger.error("Token verification failed.")

# Note: Ensure that the JWT_SECRET_KEY and JWT_ALGORITHM environment variables are set securely in your deployment environment.
#       Do not log sensitive information such as the contents of the token.
#       Implement key rotation and secure transmission protocols (e.g., HTTPS) as part of your overall security strategy.

