import os
import uuid
import mysql.connector
from mysql.connector import Error
from werkzeug.utils import secure_filename

# Configuration for MySQL connection
config = {
    'user': 'limited_user',  # User with limited privileges
    'password': 'password',  # Strong password for the user
    'host': 'localhost',
    'database': 'image_database',
    'raise_on_warnings': True
}

# Connect to the database
try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print('Connected to MySQL database')
except Error as e:
    print(f"Error: {e}")
    exit(1)

# Function to store image in the database
def store_image(image_path):
    # Generate a unique filename to avoid conflicts and enforce case-insensitivity
    _, file_extension = os.path.splitext(image_path)
    file_extension = file_extension.lower()  # Enforce case-insensitivity
    unique_filename = secure_filename(str(uuid.uuid4()) + file_extension)

    # Read image file in binary mode
    with open(image_path, 'rb') as file:
        binary_data = file.read()

    try:
        cursor = connection.cursor()
        # Use a prepared statement to securely insert the image
        query = "INSERT INTO images (filename, image_data) VALUES (%s, %s)"
        cursor.execute(query, (unique_filename, binary_data))
        connection.commit()
        print(f"Image {unique_filename} stored successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

# Function to create a user with limited privileges
def create_limited_user(username, password):
    try:
        cursor = connection.cursor()
        # Create a new user with limited privileges
        cursor.execute(f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}';")
        cursor.execute(f"GRANT INSERT ON image_database.images TO '{username}'@'localhost';")
        connection.commit()
        print(f"User {username} created with limited privileges.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

# Replace 'path_to_image.jpg' with the path to the image you want to upload
image_path = 'path_to_image.jpg'
store_image(image_path)

# Create a new user with limited privileges
# Note: Replace 'new_user' and 'strong_password' with the desired username and a strong password
create_limited_user('new_user', 'strong_password')

# Close the database connection
if connection.is_connected():
    connection.close()
    print('MySQL connection is closed')

