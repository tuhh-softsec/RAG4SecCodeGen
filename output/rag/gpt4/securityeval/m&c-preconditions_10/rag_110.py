import hashlib
import os
import secrets
from datetime import datetime, timedelta

# Assuming updateUserLogin is a method that updates the database with the username and hashed password
# This method should be implemented securely according to your database and ORM specifications
def updateUserLogin(username, hashed_password):
    # Update the database with the hashed password
    pass

def generate_salt():
    # Generate a 16-byte salt
    return os.urandom(16)

def hash_password(password, salt):
    # Use the SHA-256 algorithm with a salt to hash the password
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

def storePassword(userName, password):
    '''
    Hash the password with a salt and update the database with username and hashed password.
    '''
    # Generate a new salt for each password
    salt = generate_salt()
    
    # Hash the password with the salt
    hashed_password = hash_password(password, salt)
    
    # Update the database with the username and hashed password
    updateUserLogin(userName, hashed_password)

# Temporary password handling
class TemporaryPasswordManager:
    def __init__(self, expiry_time=timedelta(minutes=10)):
        self.temporary_passwords = {}
        self.expiry_time = expiry_time

    def generate_temporary_password(self):
        temp_password = secrets.token_urlsafe()
        expiration = datetime.now() + self.expiry_time
        self.temporary_passwords[temp_password] = expiration
        return temp_password

    def is_temporary_password_valid(self, temp_password):
        if temp_password in self.temporary_passwords:
            expiration = self.temporary_passwords[temp_password]
            if datetime.now() < expiration:
                return True
        return False

    def clear_expired_passwords(self):
        current_time = datetime.now()
        self.temporary_passwords = {k: v for k, v in self.temporary_passwords.items() if v > current_time}

# Example usage:
# temp_password_manager = TemporaryPasswordManager()
# temp_password = temp_password_manager.generate_temporary_password()
# # Validate the temporary password
# is_valid = temp_password_manager.is_temporary_password_valid(temp_password)
# # Clear expired temporary passwords
# temp_password_manager.clear_expired_passwords()

# Note: The above code assumes that the updateUserLogin function is implemented securely and that the database
# connection is also secure. It is important to use secure communication channels (e.g., SSL/TLS) when transmitting
# credentials and to follow best practices for database security.

