import os
from hashlib import pbkdf2_hmac
from hmac import compare_digest
from datetime import datetime, timedelta
from threading import Lock
import logging
import time

# Constants for PBKDF2
HASH_NAME = 'sha256'  # Hashing algorithm to use
ITERATIONS = 100000   # Number of iterations for PBKDF2
KEY_LENGTH = 32       # Length of the derived key

# Secure storage for temporary passwords and their expiration times
# This should be replaced with a thread-safe, persistent storage solution
# with encryption at rest, such as a secure database.
temporary_passwords = {}
passwords_lock = Lock()

# Configure logging to avoid storing sensitive information
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to securely delete a password from memory
# Note: This is a placeholder function. Python does not guarantee secure deletion of memory.
# Consider using a dedicated library or secure hardware module for handling sensitive data.
def secure_delete(user_id):
    with passwords_lock:
        if user_id in temporary_passwords:
            del temporary_passwords[user_id]

def generate_salt():
    """
    Generates a random salt.
    """
    return os.urandom(16)  # 16 bytes salt

def get_hash(password, salt=None):
    """
    Create a hash of the password with a salt.
    """
    if salt is None:
        salt = generate_salt()  # Generate a new salt for each password
    hash_value = pbkdf2_hmac(HASH_NAME, password.encode(), salt, ITERATIONS, KEY_LENGTH)
    return salt, hash_value

def store_temporary_password(user_id, password):
    """
    Stores a temporary password in a thread-safe manner with an expiration time.
    """
    # Input validation for user_id and password
    if not isinstance(user_id, str) or not isinstance(password, str):
        raise ValueError("User ID and password must be strings.")
    if user_id == "" or password == "":
        raise ValueError("User ID and password cannot be empty.")

    # Enforce strong password policy (placeholder, implement actual policy checks)
    if len(password) < 8:
        raise ValueError("Password does not meet complexity requirements.")

    salt, hash_value = get_hash(password)
    expiration_time = time.monotonic() + 300  # Temporary password valid for 5 minutes
    with passwords_lock:
        temporary_passwords[user_id] = (salt, hash_value, expiration_time)
    logging.info(f"Temporary password stored for user {user_id}")

def is_temporary_password_valid(user_id, password):
    """
    Checks if the temporary password is valid and has not expired in a thread-safe manner.
    """
    with passwords_lock:
        if user_id not in temporary_passwords:
            return False
        salt, stored_hash, expiration_time = temporary_passwords[user_id]
        if time.monotonic() > expiration_time:
            secure_delete(user_id)  # Remove expired password securely
            return False
        hash_value = pbkdf2_hmac(HASH_NAME, password.encode(), salt, ITERATIONS, KEY_LENGTH)
        valid = compare_digest(stored_hash, hash_value)
        if not valid:
            logging.warning(f"Invalid password attempt for user {user_id}")
        return valid

# Example usage
if __name__ == "__main__":
    user_password = "secure_password"
    user_id = "user123"

    # Store a temporary password
    store_temporary_password(user_id, user_password)

    # Validate the temporary password
    if is_temporary_password_valid(user_id, user_password):
        print("Temporary password is valid.")
    else:
        print("Temporary password is invalid or has expired.")

