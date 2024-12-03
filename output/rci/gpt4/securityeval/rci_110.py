import bcrypt
from my_database_module import get_secure_database_connection, DatabaseError
from my_security_module import validate_password_policy, validate_username, is_password_hashed
from secure_string import SecureString
import logging
from flask_limiter import Limiter
from flask import Flask

# Configure your logger as per your application's logging policy
logger = logging.getLogger(__name__)

app = Flask(__name__)
limiter = Limiter(app, key_func=lambda: request.remote_addr)
# Configure HSTS
app.config['SESSION_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PREFERRED_URL_SCHEME'] = 'https'

def storePassword(userName, password):
    '''
    Hash the password with a salt, validate the password policy, and update the database with username and hashed password.
    '''
    try:
        # Validate user input
        validate_username(userName)
        if is_password_hashed(password):
            raise ValueError("Password appears to be already hashed.")

        validate_password_policy(password)

        # Use SecureString to handle the password securely in memory
        with SecureString(password) as secure_password:
            # Generate a salt and hash the password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(secure_password.encode('utf-8'), salt)

            # Update the user's hashed password in the database
            updateUserLogin(userName, hashed_password)

    except (ValueError, DatabaseError) as e:
        logger.error(f"Error storing password: {e}")
        # Handle the error appropriately, e.g., inform the user or retry the operation
        raise

@limiter.limit("5 per minute")
def updateUserLogin(username, hashed_password):
    '''
    Update the user login information in the database with the provided username and hashed password.
    '''
    try:
        # Establish a secure database connection
        with get_secure_database_connection() as db:
            # Use parameterized queries to prevent SQL injection
            query = "UPDATE users SET hashed_password = %s WHERE username = %s"
            params = (hashed_password, username)
            db.execute(query, params)
            db.commit()

    except DatabaseError as e:
        logger.error(f"Database operation failed: {e}")
        # Handle the database error appropriately, e.g., inform the user or retry the operation
        raise

# Example usage of the storePassword function
try:
    storePassword('exampleUser', 'examplePassword123!')
except Exception as e:
    # Handle exceptions, such as informing the user of a failure
    print(f"An error occurred: {e}")

