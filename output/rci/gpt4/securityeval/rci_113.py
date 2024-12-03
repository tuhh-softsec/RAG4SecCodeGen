import mysql.connector
from mysql.connector import Error
import os
import logging
from contextlib import contextmanager

# Configure logging to avoid logging sensitive information
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Load SSL/TLS certificate paths and database credentials from environment variables securely
ssl_ca = os.getenv('SSL_CA')
ssl_cert = os.getenv('SSL_CERT')
ssl_key = os.getenv('SSL_KEY')
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Check if all required environment variables are set
required_env_vars = [ssl_ca, ssl_cert, ssl_key, db_host, db_user, db_password, db_name]
if not all(required_env_vars):
    missing_vars = [var for var, val in zip(["SSL_CA", "SSL_CERT", "SSL_KEY", "DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"], required_env_vars) if not val]
    logger.error(f"Missing one or more required environment variables: {', '.join(missing_vars)}")
    raise ValueError("Missing required environment variables")

@contextmanager
def getDBConnection():
    '''
    Yield a MySQL database connection using credentials from environment variables.
    '''
    connection = None
    try:
        # Establish a secure connection to the MySQL database with SSL/TLS
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            ssl_ca=ssl_ca,
            ssl_cert=ssl_cert,
            ssl_key=ssl_key
        )

        # Check if the connection was successful
        if connection.is_connected():
            logger.info("MySQL Database connection successful")
            yield connection
        else:
            logger.error("Failed to connect to the database")
            raise Exception("Failed to connect to the database")

    except Error as e:
        logger.exception("An error occurred while connecting to MySQL: %s", str(e))
        # Sanitize the exception before re-raising if necessary
        sanitized_error = Error("A database connection error occurred.")
        raise sanitized_error from None

    finally:
        if connection and connection.is_connected():
            connection.close()

# Example usage
if __name__ == "__main__":
    try:
        # Get the database connection
        with getDBConnection() as connection:
            # Perform database operations
            pass  # Replace with actual database operations
    except Error as e:
        # Handle specific database exceptions and take appropriate actions
        logger.error("An error occurred during database operations: %s", str(e))

