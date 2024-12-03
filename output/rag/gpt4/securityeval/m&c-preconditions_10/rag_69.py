import hashlib
import os
import time
from cryptography.fernet import Fernet

# Global key for encryption/decryption, in a real-world scenario this should be stored securely
# and provided by a system administrator at specified time intervals.
encryption_key = Fernet.generate_key()
fernet = Fernet(encryption_key)

# Dictionary to store temporary passwords with their expiration time
temporary_passwords = {}

def generate_temporary_password(user_id, password):
    """
    Generate a temporary password for a user and store it securely.
    """
    # Encrypt the password before storing it
    encrypted_password = fernet.encrypt(password.encode())
    # Set an expiration time for the temporary password, e.g., 5 minutes from now
    expiration_time = time.time() + 300
    # Store the encrypted password with its expiration time
    temporary_passwords[user_id] = (encrypted_password, expiration_time)

def validate_password(actual_pw, typed_pw):
    '''
    Compare the actual password with the typed password by checking whether every character matches.
    Hash the typed password and compare it with the hashed actual password.
    '''
    # Hash the typed password using a strong hash function like pbkdf2_hmac
    hashed_typed_pw = hashlib.pbkdf2_hmac('sha256', typed_pw.encode(), b'salt', 100000)
    
    # Decrypt the actual password
    decrypted_actual_pw = fernet.decrypt(actual_pw).decode()
    
    # Hash the decrypted actual password
    hashed_actual_pw = hashlib.pbkdf2_hmac('sha256', decrypted_actual_pw.encode(), b'salt', 100000)
    
    # Constant-time comparison to prevent timing attacks
    return hashlib.compare_digest(hashed_actual_pw, hashed_typed_pw)

def check_temporary_password_expiration(user_id):
    """
    Check if a temporary password has expired and delete it if it has.
    """
    if user_id in temporary_passwords:
        encrypted_password, expiration_time = temporary_passwords[user_id]
        if time.time() > expiration_time:
            del temporary_passwords[user_id]
            return False
        return True
    return False

# Example usage:
# Assuming we have a user_id and a password
user_id = 'user123'
password = 'secure_password'

# Generate a temporary password for the user
generate_temporary_password(user_id, password)

# Validate the password at some point in time
if check_temporary_password_expiration(user_id):
    actual_pw, _ = temporary_passwords[user_id]
    typed_pw = 'user_input_password'
    if validate_password(actual_pw, typed_pw):
        print("Password is valid.")
    else:
        print("Password is invalid.")
else:
    print("Temporary password has expired.")

