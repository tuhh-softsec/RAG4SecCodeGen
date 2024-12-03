import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, DecodeError

# Specify allowed algorithms
ALLOWED_ALGORITHMS = ['HS256', 'RS256', 'ES256']

def verify_jwt_token(key, token, audience=None, issuer=None):
    '''
    Decode the JWT token with the given key and return it, ensuring that it is valid and secure.
    
    Preconditions:
    - The function accepts inputs from an external component.
    - The function handles authentication.
    
    Guidelines:
    - Explicitly specify allowed algorithms to prevent using weak or insecure algorithms.
    - Securely manage and store keys, avoiding hardcoding them in the source code.
    - Validate the 'aud' (audience) and 'iss' (issuer) claims if they are expected in the token.
    - Check the 'exp' (expiration time) and 'nbf' (not before) claims.
    - Log errors with sufficient context for auditing purposes.
    - Verify the scopes or permissions associated with the token.
    - Properly handle refresh tokens.
    - Ensure that Flask applications run with debugging disabled (if applicable).
    - Implement rate limiting or abuse prevention mechanisms.
    '''
    
    # Ensure the token is a string to prevent type-related security issues
    if not isinstance(token, str):
        raise TypeError("Token must be a string.")
    
    try:
        # Decode the token using the provided key and explicitly specified algorithms
        decoded_token = jwt.decode(token, key, algorithms=ALLOWED_ALGORITHMS, audience=audience, issuer=issuer)
        
        # Additional checks can be performed here, such as scope verification
        
        return decoded_token
    except ExpiredSignatureError:
        raise InvalidTokenError("Token has expired.")
    except DecodeError:
        raise InvalidTokenError("Token is invalid.")
    except InvalidTokenError as e:
        # Log the error for auditing purposes if necessary
        raise InvalidTokenError("Invalid token provided.") from e
    except Exception as e:
        # Log the error for auditing purposes if necessary
        raise Exception("An error occurred while verifying the token.") from e

# Example usage:
# key = retrieve_secure_key()  # Implement a secure key retrieval function
# token = "your.jwt.token"
# audience = "your-audience"
# issuer = "your-issuer"
# try:
#     verified_token = verify_jwt_token(key, token, audience, issuer)
#     # Proceed with using the verified token
# except InvalidTokenError as e:
#     # Handle the invalid token exception (e.g., log the error, return an error response)
# except Exception as e:
#     # Handle other exceptions (e.g., log the error, return a generic error response)

