import bcrypt
import MySQLdb
from MySQLdb.cursors import DictCursor
import os
import logging
from contextlib import closing
import sys

# Configure your database connection here
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER'),
    'passwd': os.getenv('DB_PASS'),
    'db': os.getenv('DB_NAME'),
    'charset': 'utf8mb4',
    'ssl': {'ca': os.getenv('DB_SSL_CA'), 'cert': os.getenv('DB_SSL_CERT'), 'key': os.getenv('DB_SSL_KEY')}
}

# Set up logging
log_file_path = os.getenv('LOG_FILE_PATH', 'login_attempts.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def checkPassword(userid, password):
    '''
    Get the hashed password of the userid from the database and compare with the provided one.
    '''
    # Connect to the database using a context manager to ensure proper resource management
    with closing(MySQLdb.connect(**db_config, cursorclass=DictCursor)) as db, closing(db.cursor()) as cursor:
        try:
            # Use a parameterized query to prevent SQL injection
            cursor.execute("SELECT password_hash FROM users WHERE userid = %s", (userid,))
            user_record = cursor.fetchone()

            if user_record:
                # Fetch the stored password hash
                password_hash = user_record['password_hash']

                # Use bcrypt to check the provided password against the hashed password
                if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
                    logging.info(f"Login successful for user: {userid}")
                    return True  # The password is correct
                else:
                    logging.warning(f"Login failed for user: {userid}")
                    return False  # The password is incorrect
            else:
                logging.warning(f"Login failed for user: {userid}")
                return False  # User not found

        except MySQLdb.Error as e:
            logging.error(f"Database error: {e}")
            # Alert administrators or trigger monitoring system here
            # e.g., send_email_to_admin(e) or trigger_monitoring_alert(e)
            return False

# Example usage:
# userid = 'some_user_id'
# password = 'user_password'
# if checkPassword(userid, password):
#     print("Login successful")
# else:
#     print("Login failed")

# Note: Do not print different messages for login success or failure in production to avoid user enumeration.

