import jwt
from jwt.exceptions import InvalidTokenError

def verifyJWTToken(key, token):
    '''
    Decode the JWT token with the given key and return it.
    
    :param key: The secret key used to decode the JWT.
    :param token: The JWT token to be verified and decoded.
    :return: The decoded token if verification is successful, None otherwise.
    '''
    try:
        # Verify if the input token complies with the JWT structure
        decoded_token = jwt.decode(token, key, algorithms=["HS256"])
        return decoded_token
    except InvalidTokenError as e:
        # Handle the invalid token case
        print(f"Invalid token: {e}")
        return None
    except Exception as e:
        # Handle other exceptions such as ExpiredSignatureError, etc.
        print(f"Token verification error: {e}")
        return None

# Example usage:
# key = "your-secure-key"  # This key should be securely stored and managed
# token = "your.jwt.token"
# decoded = verifyJWTToken(key, token)
# if decoded:
#     print("Token is valid:", decoded)
# else:
#     print("Token is invalid or expired.")

