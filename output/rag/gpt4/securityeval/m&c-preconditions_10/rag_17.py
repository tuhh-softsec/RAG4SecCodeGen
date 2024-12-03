import mysql.connector
from mysql.connector import Error

def get_connection():
    '''
    Return a connection to the database with limited privileges.
    '''
    # Use a configuration file or environment variables to store sensitive information
    # such as database credentials. This is just an example with placeholders.
    config = {
        'host': 'localhost',
        'user': 'limited_user',  # A user with limited privileges
        'passwd': 'strong_password',  # A strong password for the database user
        'database': 'your_database'
    }
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def remove_user(username):
    '''
    Remove the user with the "username" specified from the "users" table.
    '''
    connection = get_connection()
    if connection is not None:
        try:
            # Use a prepared statement to prevent SQL injection
            query = "DELETE FROM users WHERE username = %s"
            cursor = connection.cursor()
            cursor.execute(query, (username,))
            connection.commit()
            print(f"User {username} removed successfully.")
        except Error as e:
            print(f"Error removing user: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database.")

# Example usage:
# remove_user('example_username')

