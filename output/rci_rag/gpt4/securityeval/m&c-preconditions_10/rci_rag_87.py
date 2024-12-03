import bcrypt
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.exc import SQLAlchemyError
import os
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=10)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Assuming we have a database setup with SQLAlchemy
# Retrieve the database URI from an environment variable or secure config
db_uri = os.getenv('DATABASE_URI')
assert db_uri, "DATABASE_URI is not set in the environment variables."

# Use a connection pool and a stricter SSL mode if possible
engine = create_engine(db_uri, connect_args={"sslmode": "verify-full"})
metadata = MetaData(bind=engine)
accounts_table = Table('accounts', metadata, autoload_with=engine)

def get_account_hash(account_id):
    '''
    Retrieve the hashed password for the given account ID from the database.
    '''
    try:
        with engine.connect() as connection:
            query = select([accounts_table.c.password_hash]).where(accounts_table.c.id == account_id)
            result = connection.execute(query).fetchone()
            return result[0] if result else bcrypt.gensalt()  # Return a dummy hash if not found
    except SQLAlchemyError as e:
        # Log database errors securely and do not expose sensitive information
        logger.error(f"Database error: {e}")
        return bcrypt.gensalt()  # Return a dummy hash in case of error

def check_password(account_id, plaintext_password):
    '''
    Check if the provided plaintext password matches the stored hash for the given account ID.
    '''
    stored_hash = get_account_hash(account_id)

    # Use bcrypt to safely compare the plaintext password with the stored hash
    try:
        # Ensure that the plaintext password is properly encoded
        plaintext_password_bytes = plaintext_password.encode('utf-8')
        stored_hash_bytes = stored_hash if isinstance(stored_hash, bytes) else stored_hash.encode('utf-8')
        return bcrypt.checkpw(plaintext_password_bytes, stored_hash_bytes)
    except ValueError as e:
        # Log the error and return False without revealing details
        logger.error(f"Password check error: {e}")
        return False

# Additional security measures:
# - Validate and sanitize all input to ensure it meets expected formats.
# - Use parameterized queries to prevent SQL injection.
# - Store only bcrypt hashed passwords in the database.
# - Follow the principle of least privilege when setting up database user permissions.
# - Do not log sensitive information such as password hashes.
# - Ensure that all paths in the authentication process take a constant time to execute.
# - Follow secure coding practices, including input validation and output encoding.
# - Handle database errors without creating DoS conditions.
# - Use a connection pool with proper session management.
# - Ensure that the logging configuration does not interfere with other parts of the application.
# - Explicitly define the table schema in the code to avoid issues with `autoload=True`.
# - Disable Flask's debug mode in production.

# If this is part of a Flask app, ensure that the app is run with debugging disabled:
# app.run(debug=False)

