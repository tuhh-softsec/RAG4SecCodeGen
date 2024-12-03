import bcrypt
import logging
from getpass import getpass  # Use getpass to securely prompt for password input

# Configure logging
logging.basicConfig(filename='admin_login.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Function to hash a password
def hash_password(password):
    '''
    Hash a password for storing.
    '''
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Function to check the password against the hashed password
def check_admin_password(password, hashed_password):
    '''
    Check if the password is valid for an admin user.
    '''
    try:
        # Check if the password matches the hashed password
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    except bcrypt.exceptions.BcryptError as e:
        # Log the exception with an appropriate level of detail
        logging.error("Bcrypt error occurred: %s", e)
        return False
    except ValueError as e:
        # Handle specific exceptions related to password checking
        logging.error("Value error: %s", e)
        return False

# Example usage:
# In a real scenario, the hashed password would be retrieved from a secure database
# The database should be secured with access controls, encryption at rest, and secure communication channels
# The password input should be sanitized and validated
# Implement logging for failed login attempts and other security events
# Ensure passwords are transmitted over encrypted channels (e.g., HTTPS)

# Prompt for the admin password securely
admin_password = getpass("Enter admin password for hashing: ")
admin_hashed_password = hash_password(admin_password)

# Prompt for the password to check
password_to_check = getpass("Enter password to check: ")
is_correct = check_admin_password(password_to_check, admin_hashed_password)

# Output the result
print("Admin password is correct:", is_correct)

# Note: In production, you would also implement rate limiting, account lockout, and a strong password policy.
# Additionally, manage the bcrypt salt securely and configure the bcrypt work factor based on your server's capabilities.

