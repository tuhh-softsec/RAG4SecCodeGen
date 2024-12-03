import mysql.connector
from mysql.connector import pooling

# Define database configuration
db_config = {
    'user': 'secure_user',  # Use a user with the least privileges necessary
    'password': 'strong_password',  # Use a strong password
    'host': 'localhost',
    'database': 'secure_db',
    'raise_on_warnings': True,
    'use_pure': True
}

# Define a connection pool with limited number of connections
connection_pool = pooling.MySQLConnectionPool(pool_name="mypool",
                                              pool_size=5,  # Limit the number of connections
                                              pool_reset_session=True,
                                              **db_config)

def getConnection():
    '''
    Return a connection object for a MySQL database from the connection pool.
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
    conn = getConnection()
    if conn:
        # Perform database operations using prepared statements or query parameters
        cursor = conn.cursor(prepared=True)
        query = "SELECT * FROM secure_table WHERE id = %s"
        cursor.execute(query, (some_id,))  # Use query parameters to prevent SQL injection
        # Cache the result set if necessary
        result = cursor.fetchall()
        cursor.close()
        conn.close()

