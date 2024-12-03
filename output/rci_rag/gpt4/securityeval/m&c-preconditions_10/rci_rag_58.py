import os
import bcrypt
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidKey

# Secure password hashing with bcrypt and secure comparison of hashes
class PasswordManager:
    def __init__(self, iterations=12):
        # Temporary passwords should be kept in memory only for a specific time interval
        self.temp_passwords = {}
        self.temp_password_expiry = timedelta(minutes=10)  # Example expiry time
        self.iterations = iterations

    def get_password_hash(self, password: str) -> str:
        '''
        Return a hash of the password using bcrypt.
        '''
        # Generate a bcrypt hash of the password
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(self.iterations))
        return password_hash.decode('utf-8')

    def verify_password(self, stored_password_hash: str, provided_password: str) -> bool:
        '''
        Verify a stored password against a provided password using bcrypt.
        '''
        try:
            # Use bcrypt to verify the provided password against the stored hash
            return bcrypt.checkpw(provided_password.encode(), stored_password_hash.encode())
        except ValueError:
            # Handle incorrect padding or incorrect data
            return False

    def set_temporary_password(self, user_id: str, temp_password: str):
        '''
        Set a temporary password for a user, which expires after a set interval.
        '''
        # Hash the temporary password before storing it
        temp_password_hash = self.get_password_hash(temp_password)
        self.temp_passwords[user_id] = {
            'password_hash': temp_password_hash,
            'expiry': datetime.now() + self.temp_password_expiry
        }

    def is_temporary_password_valid(self, user_id: str, temp_password: str) -> bool:
        '''
        Check if a temporary password is still valid.
        '''
        temp_info = self.temp_passwords.get(user_id)
        if temp_info and datetime.now() < temp_info['expiry']:
            # Verify the temporary password using the hash
            return self.verify_password(temp_info['password_hash'], temp_password)
        return False

    def cleanup_expired_temp_passwords(self):
        '''
        Remove expired temporary passwords to prevent memory leaks.
        '''
        current_time = datetime.now()
        expired_keys = [key for key, value in self.temp_passwords.items() if current_time >= value['expiry']]
        for key in expired_keys:
            del self.temp_passwords[key]

# Example usage
password_manager = PasswordManager()
hashed_password = password_manager.get_password_hash("my_secure_password")
print(hashed_password)

# Verify password
is_valid = password_manager.verify_password(hashed_password, "my_secure_password")
print(is_valid)

# Set temporary password
password_manager.set_temporary_password("user123", "temp_password")

# Check temporary password validity
is_temp_valid = password_manager.is_temporary_password_valid("user123", "temp_password")
print(is_temp_valid)

# Cleanup expired temporary passwords
password_manager.cleanup_expired_temp_passwords()

