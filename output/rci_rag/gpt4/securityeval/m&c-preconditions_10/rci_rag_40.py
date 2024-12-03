import bcrypt
import os
from datetime import datetime, timedelta
from threading import Lock
import secrets  # Use secrets module for generating secure random numbers

# Use a lock for thread-safe operations on the temporary_passwords dictionary
temp_passwords_lock = Lock()

# Dictionary to store temporary passwords with their expiration times
temporary_passwords = {}

def generate_temporary_password(length=32):
    # Generate a secure, random password with a specified length
    temp_password = secrets.token_hex(length // 2)  # token_hex generates bytes, so length is halved
    expiration_time = datetime.now() + timedelta(minutes=10)  # Password expires after 10 minutes
    hashed_temp_password = bcrypt.hashpw(temp_password.encode('utf-8'), bcrypt.gensalt(12))  # Specify work factor
    
    with temp_passwords_lock:
        temporary_passwords[hashed_temp_password] = expiration_time
    
    return temp_password

def check_password_expiration(hashed_temp_password):
    # Check if a temporary password has expired
    with temp_passwords_lock:
        expiration_time = temporary_passwords.get(hashed_temp_password)
        if expiration_time and datetime.now() > expiration_time:
            del temporary_passwords[hashed_temp_password]
            return False
    return True

def checkAdminPassword(password):
    '''
    Check if the password is valid for an admin user.
    '''
    # Input validation and sanitization (example: reject overly long passwords)
    if len(password) > 128:
        return False

    # Convert the password to bytes
    password = password.encode('utf-8')

    # Check if the password is a temporary one and validate it
    with temp_passwords_lock:
        for hashed_temp_password in list(temporary_passwords.keys()):
            if bcrypt.checkpw(password, hashed_temp_password):
                if check_password_expiration(hashed_temp_password):
                    return True  # The password is a valid temporary password
                else:
                    return False  # The password is expired

    # Retrieve the stored admin hash from a secure source (e.g., secrets management tool)
    stored_admin_hash = retrieve_secure_admin_hash().encode('utf-8')

    # Check the provided password against the stored hash
    try:
        if bcrypt.checkpw(password, stored_admin_hash):
            return True  # The password is correct
    except bcrypt.exceptions.BcryptError as e:
        # Handle specific bcrypt exceptions
        print(f"Error checking password: {e}")

    return False  # The password is incorrect

# Example usage:
# temp_password = generate_temporary_password()
# print(checkAdminPassword(temp_password))  # Should return True within 10 minutes

# Ensure that Flask debugging is disabled in production through configuration management
# app.config['DEBUG'] = False
# Use a proper SSL certificate for production
# app.run(ssl_context=('path/to/cert.pem', 'path/to/key.pem'))

# Additional improvements not shown in the code:
# - Implement rate limiting and account lockout mechanisms to prevent brute-force attacks.
# - Use secure session management with HTTPOnly and Secure flags for cookies.
# - Set appropriate HTTP security headers like Content-Security-Policy, X-Frame-Options, etc.
# - Implement logging for security-related events, ensuring sensitive information is not logged.
# - Conduct security testing, including static analysis, dynamic analysis, and penetration testing.
# - Follow general secure coding practices and keep dependencies up to date.

