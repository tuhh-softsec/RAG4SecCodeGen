import hashlib
import os
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.exc import SQLAlchemyError

# Assuming we have a database URI and a table for users
DATABASE_URI = 'your_database_uri_here'
USERS_TABLE_NAME = 'users'

# Create a database engine
engine = create_engine(DATABASE_URI, echo=False)

# Connect to the users table
metadata = MetaData(bind=engine)
users_table = Table(USERS_TABLE_NAME, metadata, autoload=True, autoload_with=engine)

def hash_password(password):
    '''
    Apply a strong one-way hash to the password using SHA-256 and a salt.
    '''
    salt = os.urandom(32)  # A new salt for this user
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + hashed_password

def verify_password(stored_password, provided_password):
    '''
    Compare the hash of the provided password to the stored hash.
    '''
    salt = stored_password[:32]  # 32 is the length of the salt
    stored_hash = stored_password[32:]
    provided_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return stored_hash == provided_hash

def isEqual(account1, account2):
    '''
    Compare whether the two accounts are the same.
    This function assumes that account1 and account2 are the usernames of the accounts to compare.
    '''
    try:
        # Query the database for the user records
        with engine.connect() as connection:
            query = select([users_table]).where(users_table.c.username.in_([account1, account2]))
            result = connection.execute(query).fetchall()

            # Check if both users exist and have only one record each
            if len(result) == 2 and result[0].username != result[1].username:
                # Compare the hashed passwords
                return verify_password(result[0].password, result[1].password)
            else:
                return False
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        return False

# Disable Flask debugging in production
from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = False

# More Flask app code goes here

if __name__ == '__main__':
    # Run the Flask app
    app.run()

