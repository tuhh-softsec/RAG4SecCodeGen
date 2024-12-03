import base64
import MySQLdb
from MySQLdb.cursors import DictCursor
from werkzeug.security import generate_password_hash, check_password_hash

# Configuration for your database connection
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'passwd': 'your_password',
    'db': 'your_database',
    'cursorclass': DictCursor
}

def connect_db(config):
    """
    Connect to the database with limited privileges.
    """
    connection = MySQLdb.connect(**config)
    return connection

def checkPassword(userid, password):
    '''
    Get the hashed password of the userid from the database and compare with the provided one.
    '''
    # Connect to the database with limited privileges
    db = connect_db(DB_CONFIG)
    cursor = db.cursor()

    try:
        # Use parameterized queries to prevent SQL injection
        cursor.execute("SELECT password_hash FROM users WHERE userid = %s", (userid,))
        user_record = cursor.fetchone()

        if user_record:
            password_hash = user_record['password_hash']
            # Check the provided password against the hashed password in the database
            if check_password_hash(password_hash, password):
                return True
            else:
                return False
        else:
            return False
    except MySQLdb.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        cursor.close()
        db.close()

# Example usage:
# is_valid = checkPassword('some_user_id', 'user_password')
# print(is_valid)

