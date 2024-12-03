import mysql.connector
from mysql.connector import pooling

# Define database configuration
db_config = {
    'user': 'secure_user',  # Use a user with the least privileges necessary
    'password': 'strong_password',  # Use a strong password
    'host': 'localhost',
    'database': 'secure_db',
    'raise_on_warnings': True
}

# Create a connection pool with limited number of connections
connection_pool = pooling.MySQLConnectionPool(pool_name="mypool",
                                             pool_size=5,  # Limit the number of connections
                                             pool_reset_session=True,
                                             **db_config)

def getDBConnection():
    '''
    Return a MySQL database connection from the pool.
    '''
    try:
        # Get connection from the connection pool
        connection = connection_pool.get_connection()
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Example usage
if __name__ == "__main__":
    # Get a database connection
    db_conn = getDBConnection()
    if db_conn:
        try:
            # Create a cursor object using the cursor() method
            cursor = db_conn.cursor(prepared=True)  # Use prepared statements for security
            
            # Prepare SQL query to read data from the database
            query = "SELECT * FROM secure_table WHERE id = %s"
            cursor.execute(query, (1,))  # Use query parameters to prevent SQL injection
            
            # Fetch and cache all rows in a list
            results = cursor.fetchall()
            
            # Process the results
            for row in results:
                print(row)
            
            # Close the cursor
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        finally:
            # Close the connection
            db_conn.close()

