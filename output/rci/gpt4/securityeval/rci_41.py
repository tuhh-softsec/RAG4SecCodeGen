import mysql.connector
import os
import logging
from mysql.connector import Error

# Configure logging with restricted file permissions
logging.basicConfig(filename='db_errors.log', level=logging.ERROR, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

def getConnection():
    '''
    Return a connection object for a MySQL database with improved security.
    '''
    connection = None
    try:
        # Use environment variables to store sensitive information
        db_host = os.getenv('DB_HOST')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_name = os.getenv('DB_NAME')

        # Ensure that the necessary environment variables are set
        if not all([db_host, db_user, db_password, db_name]):
            raise ValueError("Database configuration is incomplete. Please set all required environment variables.")

        # Paths to SSL certificate files
        ssl_ca = os.getenv('DB_SSL_CA')
        ssl_cert = os.getenv('DB_SSL_CERT')
        ssl_key = os.getenv('DB_SSL_KEY')

        # Check if the SSL certificate paths are provided and exist
        if not all([ssl_ca, ssl_cert, ssl_key]):
            raise FileNotFoundError("SSL certificate paths are not provided or files do not exist.")

        # Establish a secure connection enforcing SSL
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            ssl_ca=ssl_ca,
            ssl_cert=ssl_cert,
            ssl_key=ssl_key,
            ssl_verify_cert=True  # Enforce server certificate verification
        )

        # Check if the connection is using SSL
        if not connection.is_connected() or not connection._ssl_active:
            raise mysql.connector.errors.InterfaceError("SSL connection is required but not established.")

        return connection

    except Error as e:
        # Log the error securely instead of printing it
        logging.error(f"Error while connecting to MySQL: {e}")
    except FileNotFoundError as e:
        # Log file not found errors
        logging.error(f"SSL certificate file error: {e}")
    except Exception as e:
        # Log any other exceptions that are not anticipated
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        # Ensure that the connection is closed in case of error
        if connection and connection.is_connected():
            connection.close()

    return None

# Example usage with context management
if __name__ == "__main__":
    try:
        conn = getConnection()
        if conn:
            print("Successfully connected to the database.")
            # Perform database operations
            conn.close()
        else:
            print("Failed to connect to the database.")
    except Error as e:
        logging.error(f"Database error occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

