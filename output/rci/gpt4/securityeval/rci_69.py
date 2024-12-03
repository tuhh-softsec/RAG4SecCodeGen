import bcrypt
import hmac
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def hash_password(password, rounds=12):
    '''
    Hash a password for storing, using a specified number of rounds for the bcrypt algorithm.
    '''
    if isinstance(password, str):
        password = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=rounds)
    return bcrypt.hashpw(password, salt)

def validate_password(stored_hash, typed_pw):
    '''
    Validate the typed password against the stored hash using a constant-time comparison to prevent timing attacks.
    '''
    try:
        # Encode the typed password to bytes if it is not already
        if isinstance(typed_pw, str):
            typed_pw = typed_pw.encode('utf-8')

        # Hash the typed password with the same salt used to hash the stored password
        # bcrypt.hashpw will extract the salt from the stored_hash
        typed_hash = bcrypt.hashpw(typed_pw, stored_hash)

        # Use hmac.compare_digest for a constant-time comparison of the hashes
        return hmac.compare_digest(stored_hash, typed_hash)
    except Exception as e:
        logging.error("An error occurred during password validation: %s", e)
        # Return False or handle the exception as appropriate for your application
        return False

# Example usage:
# Store the hashed password (e.g., in a database) when the user sets or changes their password
user_password = "secure_password123"
hashed_password = hash_password(user_password)

# When validating a user's login attempt, retrieve the stored hash and compare it with the typed password
typed_password = "user_input_password"

# Instead of printing specific feedback, provide a generic message
if validate_password(hashed_password, typed_password):
    print("Login successful!")
else:
    print("Invalid username or password.")

# Note: Ensure that passwords are transmitted securely (e.g., over HTTPS) and implement additional security measures such as account lockout mechanisms, strong password policies, and multi-factor authentication. Securely store the password hashes and monitor authentication attempts for suspicious activity.

