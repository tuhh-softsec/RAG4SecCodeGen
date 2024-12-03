import mysql.connector
from mysql.connector import Error
import hashlib
import os

# Securely store database credentials in environment variables or a secure vault
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'your_username')
DB_PASS = os.getenv('DB_PASS', 'your_password')
DB_NAME = os.getenv('DB_NAME', 'your_database')

def get_connection():
    '''
    Return a connection to the database
    '''
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASS,
            database=DB_NAME
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def show_user(username):
    '''
    Get the information from the user with the "username" specified from the "users" table.
    Return the user information.
    '''
    connection = get_connection()
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            # Use parameterized queries to prevent SQL injection
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user_info = cursor.fetchone()
            return user_info
        except Error as e:
            print(f"Error fetching user data: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        return None

# Example usage
if __name__ == "__main__":
    username = input("Enter the username to fetch: ")
    user_data = show_user(username)
    if user_data:
        print("User Information:", user_data)
    else:
        print("No user found or an error occurred.")

