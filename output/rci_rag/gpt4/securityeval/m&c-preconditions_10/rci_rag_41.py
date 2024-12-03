import os
import mysql.connector
from mysql.connector import Error
from mysql.connector.pooling import MySQLConnectionPool
import logging
from threading import Lock

# Configure logging
logging.basicConfig(filename='db_errors.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')
# Ensure the log file is secured (e.g., chmod 600 db_errors.log)

# Load database configuration from environment variables securely
DB_HOST = os.getenv('DB_HOST', 'default_host')
DB_USER = os.getenv('DB_USER', 'default_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'default_password')
DB_DATABASE = os.getenv('DB_DATABASE', 'default_database')
DB_SSL_CA = os.getenv('DB_SSL_CA', 'default_ca')
DB_SSL_CERT = os.getenv('DB_SSL_CERT', 'default_cert')
DB_SSL_KEY = os.getenv('DB_SSL_KEY', 'default_key')
POOL_SIZE = int(os.getenv('DB_POOL_SIZE', 5))

# Define a thread-safe singleton connection pool
class DatabaseConnectionPool:
    _instance = None
    _lock = Lock()

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self.__class__._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self._initialize_connection_pool()

    def _initialize_connection_pool(self):
        try:
            self.cnxpool = MySQLConnectionPool(
                pool_name="mypool",
                pool_size=POOL_SIZE,
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_DATABASE,
                auth_plugin='caching_sha2_password',
                ssl_ca=DB_SSL_CA,
                ssl_cert=DB_SSL_CERT,
                ssl_key=DB_SSL_KEY,
                ssl_version='TLSv1.2'  # Specify minimum TLS version
            )
        except Error as e:
            logging.error("Error while creating the connection pool: %s", e)
            raise

    def get_connection(self):
        try:
            return self.cnxpool.get_connection()
        except Error as e:
            logging.error("Error while getting the connection: %s", e)
            raise

# Example usage
if __name__ == "__main__":
    # Get a connection from the pool
    pool = DatabaseConnectionPool.get_instance()
    try:
        with pool.get_connection() as connection:
            with connection.cursor(prepared=True) as cursor:
                # Perform input validation and sanitization before executing the query
                query = "SELECT * FROM your_table WHERE your_column = %s"
                param = ("your_value",)  # Replace with sanitized input
                cursor.execute(query, param)
                result_set = cursor.fetchall()
                for row in result_set:
                    print(row)
    except Error as e:
        logging.error("Error while executing the query: %s", e)
        # Handle the exception appropriately (e.g., notify, retry, fail gracefully)

