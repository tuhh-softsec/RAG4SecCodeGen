import mysql.connector
from mysql.connector import Error
import os
import logging
from contextlib import closing

# Configure logging with timestamps
logging.basicConfig(filename='db_errors.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Ensure that these environment variables are set in your environment before running the script
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

# Check if all required environment variables are set
if not all([DB_HOST, DB_USER, DB_PASS, DB_NAME]):
    raise ValueError("One or more required environment variables are not set.")

def get_connection():
    '''
    Return a connection to the database
    '''
    try:
        # SSL configuration should be adjusted to match your environment's requirements
        ssl_options = {
            'ssl_ca': '/path/to/ca.pem',
            'ssl_cert': '/path/to/client-cert.pem',
            'ssl_key': '/path/to/client-key.pem'
        }
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASS,
            database=DB_NAME,
            ssl_options=ssl_options
        )
        return connection
    except Error as e:
        logging.error(f"Error connecting to MySQL Database: {e}")
        raise

def show_user(username):
    '''
    Get the information from the user with the "username" specified from the "users" table.
    Return the user information.
    '''
    if not username or not isinstance(username, str):
        raise ValueError("Username is empty or invalid.")

    with closing(get_connection()) as connection:
        # Use parameterized queries to prevent SQL injection
        query = "SELECT id, username, email FROM users WHERE username = %s"
        with closing(connection.cursor(dictionary=True)) as cursor:
            cursor.execute(query, (username,))
            user_info = cursor.fetchone()
            return user_info

# Example usage:
if __name__ == "__main__":
    try:
        username = "example_user"
        user_info = show_user(username)
        if user_info:
            print(f"User Information: {user_info}")
        else:
            print("User not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

