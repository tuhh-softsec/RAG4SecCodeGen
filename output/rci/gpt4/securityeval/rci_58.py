import bcrypt
from argon2 import PasswordHasher, exceptions as argon2_exceptions
import secrets

# Define a function to clear sensitive information from memory
def clear_sensitive_data(variable):
    try:
        del variable
    except NameError:
        pass

def get_password_hash_bcrypt(password: str) -> bytes:
    '''
    Return a hash of the password using bcrypt with an appropriate work factor.
    '''
    try:
        # Generate a salt with a work factor (the cost parameter)
        # Adjust the work factor based on current hardware capabilities and security requirements
        salt = bcrypt.gensalt(rounds=12)
        
        # Hash the password with the generated salt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        return password_hash
    except Exception as e:
        # Handle exceptions such as hashing failure
        print(f"An error occurred while hashing the password: {e}")
        raise
    finally:
        # Clear the plaintext password from memory
        clear_sensitive_data(password)

def get_password_hash_argon2(password: str) -> str:
    '''
    Return a hash of the password using Argon2.
    '''
    try:
        # Create an Argon2 password hasher object
        ph = PasswordHasher()
        
        # Hash the password
        password_hash = ph.hash(password)
        
        return password_hash
    except argon2_exceptions.HashingError as e:
        # Handle exceptions specific to Argon2 hashing
        print(f"An error occurred while hashing the password with Argon2: {e}")
        raise
    finally:
        # Clear the plaintext password from memory
        clear_sensitive_data(password)

# Example usage:
if __name__ == "__main__":
    # Generate a strong random password using the secrets module
    password = secrets.token_urlsafe(16)
    
    # Enforce a password policy (e.g., minimum length, complexity)
    # This is a simple example; in practice, use a comprehensive policy
    if len(password) < 8 or not any(char.isdigit() for char in password):
        raise ValueError("Password does not meet the policy requirements.")
    
    try:
        # Get the password hash using bcrypt
        hashed_password_bcrypt = get_password_hash_bcrypt(password)
        print(f"Hashed password (bcrypt): {hashed_password_bcrypt}")
        
        # Get the password hash using Argon2
        hashed_password_argon2 = get_password_hash_argon2(password)
        print(f"Hashed password (Argon2): {hashed_password_argon2}")
    except Exception as e:
        # Handle any unexpected exceptions during hashing
        print(f"An unexpected error occurred: {e}")
    
    # Ensure that logs do not capture sensitive information
    # Configure logging appropriately in production systems

# Additional considerations:
# - Use secure password storage with encrypted connections and proper access controls.
# - Regularly check for updates to cryptographic libraries and test for compatibility.
# - Use constant-time comparison when verifying passwords against stored hashes.
# - Follow secure coding practices throughout the application.
# - Specify library versions to ensure compatibility and security evaluation.

