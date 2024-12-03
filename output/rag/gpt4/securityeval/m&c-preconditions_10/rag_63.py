import jwt
from jwt.exceptions import InvalidTokenError
import os
from dotenv import load_dotenv

# Load environment variables from a .env file for security
load_dotenv()

# Retrieve the secret key from an environment variable
# Ensure that the .env file is properly secured with file permissions
SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# Ensure that the secret key is not None or empty
if not SECRET_KEY:
    raise ValueError("Missing JWT_SECRET_KEY environment variable")

def verify_json_web_token(token):
    '''
    Decode the JSON web token passed and return it.
    '''
    try:
        # Decode the token using the secret key
        # Specify the algorithm used to sign the JWT for added security
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token
    except InvalidTokenError as e:
        # Handle the invalid token error (e.g., log the error, raise an exception, etc.)
        raise ValueError("Invalid token provided") from e

# Example usage:
# token = 'your.jwt.token'
# decoded = verify_json_web_token(token)
# print(decoded)

# Additional security measures:
# - Ensure that the JWT_SECRET_KEY is not stored in source code or version control.
# - Use file permissions to restrict access to the .env file and the script itself.
# - Encrypt the .env file or use a secure secrets management system.
# - If using Flask, ensure that the application is run with debugging disabled:
#   app.run(debug=False)

