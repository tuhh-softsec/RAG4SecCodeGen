import base64
import json
from cryptography.fernet import Fernet
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

# Use Fernet for symmetric encryption of tokens
fernet_key = Fernet.generate_key()
cipher_suite = Fernet(fernet_key)

# Use itsdangerous for signing the tokens
secret_key = 'your-secret-key'
serializer = URLSafeTimedSerializer(secret_key)

def confirmAuth(headers):
    '''
    Get AuthToken from headers, decode it with base64, and load with json to token object
    check if the token is valid and return the data in token object if it is valid.
    '''
    auth_token = headers.get('AuthToken')
    if not auth_token:
        return None  # or raise an exception

    try:
        # Decode the token from base64
        decoded_data = base64.b64decode(auth_token)
        # Decrypt the token using Fernet
        decrypted_data = cipher_suite.decrypt(decoded_data)
        # Deserialize the token using itsdangerous
        token_data = serializer.loads(decrypted_data)
        return token_data
    except (BadSignature, SignatureExpired, base64.binascii.Error, ValueError) as e:
        print(f"Token validation failed: {e}")
        return None  # or raise an exception

# Example usage:
# headers = {'AuthToken': 'your-auth-token'}
# user_data = confirmAuth(headers)
# if user_data:
#     print("Token is valid, user data:", user_data)
# else:
#     print("Invalid or expired token.")

