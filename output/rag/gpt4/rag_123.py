import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

# Function to establish a database connection using the principle of least privilege
def get_db_connection():
    # Use environment variables or a secure vault to store credentials, not hardcoded
    db_user = 'limited_user'  # A user with the least privileges necessary
    db_password = 'secure_password'
    db_host = 'localhost'
    db_name = 'mydatabase'
    
    # Establish a connection to the database
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host
    )
    return conn

# Function to check if a username exists in the database
def does_username_exist(username):
    # Establish a database connection
    conn = get_db_connection()
    
    try:
        # Create a new cursor with limited scope
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Use parameterized queries to prevent SQL injection
            query = sql.SQL("SELECT EXISTS(SELECT 1 FROM users WHERE username = %s)")
            
            # Execute the query with the provided username
            cursor.execute(query, (username,))
            
            # Fetch the result
            result = cursor.fetchone()
            
            # Check if the username exists
            exists = result['exists']
            
            return exists
    except psycopg2.Error as e:
        # Handle database errors appropriately
        print(f"Database error: {e}")
        return False
    finally:
        # Close the connection to the database
        conn.close()

# Example usage
username_to_check = 'example_user'
user_exists = does_username_exist(username_to_check)
print(f"Does the username exist? {'Yes' if user_exists else 'No'}")

