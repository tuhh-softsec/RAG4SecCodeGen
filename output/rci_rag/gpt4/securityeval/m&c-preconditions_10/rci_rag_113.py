import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
import os
import logging
from contextlib import closing
import sys

# Ensure all required environment variables are set
required_env_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_NAME', 'DB_SSL_CA', 'DB_SSL_CERT', 'DB_SSL_KEY']
for var in required_env_vars:
    if not os.getenv(var):
        logging.error(f"Environment variable {var} is not set.")
        sys.exit(f"Environment variable {var} is not set.")

# Load database configuration from environment variables
dbconfig = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'raise_on_warnings': True,
    'use_pure': True,
    'ssl_ca': os.getenv('DB_SSL_CA'),
    'ssl_cert': os.getenv('DB_SSL_CERT'),
    'ssl_key': os.getenv('DB_SSL_KEY')
}

# Validate SSL/TLS configuration
for key in ['ssl_ca', 'ssl_cert', 'ssl_key']:
    if not os.path.isfile(dbconfig[key]):
        logging.error(f"SSL/TLS configuration file {dbconfig[key]} does not exist.")
        sys.exit(f"SSL/TLS configuration file {dbconfig[key]} does not exist.")

# Configure the connection pool size
POOL_SIZE = int(os.getenv('DB_POOL_SIZE', 5))  # Default to 5 if not set

# Initialize the connection pool
cnx_pool = MySQLConnectionPool(pool_name="mypool",
                               pool_size=POOL_SIZE,
                               **dbconfig)

# Configure logging
logging.basicConfig(filename='db_errors.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get a database connection
def get_db_connection():
    try:
        return cnx_pool.get_connection()
    except mysql.connector.Error as err:
        logging.error("Error: Unable to connect to the database: %s", err)
        # Implement a retry mechanism or alert system administrators if needed
        return None

# Example usage
if __name__ == "__main__":
    with closing(get_db_connection()) as connection:
        if connection:
            try:
                with closing(connection.cursor(prepared=True)) as cursor:
                    # Example query using parameterized statements to prevent SQL injection
                    query = "SELECT * FROM your_table WHERE your_column = %s"
                    cursor.execute(query, ('your_value',))
                    results = cursor.fetchall()
                    # Process results...
            except mysql.connector.Error as err:
                logging.error("Database operation failed: %s", err)
                print("An error occurred. Please try again later.")
            finally:
                if connection.is_connected():
                    connection.close()
        else:
            print("Unable to establish a database connection. Please contact support.")

