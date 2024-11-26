import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

def is_user_moderator(username):
    # Fetch database credentials from environment variables
    db_host = os.environ.get('DB_HOST')
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')

    # Ensure that credentials are present
    if not all([db_host, db_name, db_user, db_password]):
        raise Exception("Database credentials are not set in environment variables.")

    # Connect to the database with the least privilege user account
    conn = None
    try:
        conn = psycopg2.connect(
            host=db_host,
            dbname=db_name,
            user=db_user,
            password=db_password
        )

        # Create a cursor to perform database operations
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Use parameterized query to prevent SQL injection
            query = sql.SQL("SELECT is_moderator FROM users WHERE username = %s")
            cursor.execute(query, (username,))

            # Fetch the result
            result = cursor.fetchone()

            # Check if the user is a moderator
            if result and result['is_moderator']:
                return True
            else:
                return False

    except psycopg2.DatabaseError as e:
        # Handle database connection errors
        print(f"Database error: {e}")
        return False
    finally:
        # Close the connection
        if conn is not None:
            conn.close()

# Example usage
# username = 'some_user'
# print(is_user_moderator(username))

