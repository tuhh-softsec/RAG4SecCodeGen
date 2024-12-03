import bcrypt
import os

# Securely load the admin's hashed password from an environment variable or secure config file
# For demonstration purposes, we'll assume the hashed password is stored in an environment variable
ADMIN_HASHED_PASSWORD = os.environ.get('ADMIN_HASHED_PASSWORD')

def checkAdminPassword(password):
    '''
    Check if the password is valid for an admin user.
    '''
    # Ensure the password is provided as a string
    if not isinstance(password, str):
        raise ValueError("Password must be a string.")

    # Convert the password to bytes
    password_bytes = password.encode('utf-8')

    # Check if the hashed password is available
    if ADMIN_HASHED_PASSWORD is None:
        raise ValueError("The hashed admin password is not available.")

    # Convert the stored hashed password to bytes
    hashed_password_bytes = ADMIN_HASHED_PASSWORD.encode('utf-8')

    # Use bcrypt to check the provided password against the hashed password
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

# Example usage:
# Set the environment variable ADMIN_HASHED_PASSWORD to a bcrypt hash of the actual admin password
# os.environ['ADMIN_HASHED_PASSWORD'] = bcrypt.hashpw(b'actual_admin_password', bcrypt.gensalt())

# Check if the provided password is correct
# is_correct = checkAdminPassword('provided_password')
# print(is_correct)

