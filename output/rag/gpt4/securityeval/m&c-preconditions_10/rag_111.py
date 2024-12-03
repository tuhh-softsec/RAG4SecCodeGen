import os
import hmac
from hashlib import pbkdf2_hmac
from datetime import datetime, timedelta

# Global dictionary to store temporary passwords with expiration time
temporary_passwords = {}

def generate_salt():
    # Guideline #4: Randomly assign salts for each separate hash
    return os.urandom(16)

def get_hash(password, salt=None):
    '''
    Create a hash of the password with a salt.
    '''
    if salt is None:
        salt = generate_salt()
    # Guideline #1: Do not store passwords with compression
    # Using pbkdf2_hmac with sha256 algorithm, recommended iterations and a unique salt
    hash_value = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt, hash_value

def store_temporary_password(user_id, password):
    '''
    Store a temporary password in memory with an expiration time.
    '''
    # Guideline #2: Keep temporary passwords in memory for a specific time interval
    salt, hash_value = get_hash(password)
    expiration_time = datetime.now() + timedelta(minutes=5)  # Temporary password valid for 5 minutes
    temporary_passwords[user_id] = (salt, hash_value, expiration_time)

def is_temporary_password_valid(user_id, password):
    '''
    Check if the temporary password is valid and has not expired.
    '''
    if user_id not in temporary_passwords:
        return False
    salt, stored_hash, expiration_time = temporary_passwords[user_id]
    if datetime.now() > expiration_time:
        del temporary_passwords[user_id]  # Remove expired password
        return False
    # Guideline #6: Use hmac.compare_digest() to securely check the hash value
    return hmac.compare_digest(stored_hash, pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000))

# Additional security measures can be implemented based on the specific application context.
# For example, for guideline #5, you would need to implement role-based access control in your backend.
# For guideline #7, you would need to implement proper access control checks in your code.
# For guideline #8 and #9, ensure that credentials are transmitted over secure channels (e.g., HTTPS) and are encrypted at rest.
# For guideline #10, if using Flask, ensure to set `app.debug = False` in the production environment.

