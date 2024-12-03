import os
import pwd
import grp
import subprocess
import logging

# Constants for the base directory
BASE_DIR = '/home'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def sanitize_username(username):
    # Sanitize the username to prevent directory traversal or injection attacks
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-")
    return ''.join(c for c in username if c in allowed_chars)

def create_user_directory(username, group_name):
    sanitized_username = sanitize_username(username)
    user_dir = os.path.join(BASE_DIR, sanitized_username)

    # Check if the user exists
    try:
        pwd.getpwnam(sanitized_username)
    except KeyError:
        logging.error(f"User {sanitized_username} does not exist.")
        return

    # Check for special directory names
    if sanitized_username in ['.', '..']:
        logging.error("Invalid username: '.' or '..' are not allowed.")
        return

    # Get the group ID for the specified group name
    try:
        group_id = grp.getgrnam(group_name).gr_gid
    except KeyError:
        logging.error(f"Group {group_name} does not exist.")
        return

    # Create the directory with the correct permissions and group
    try:
        os.makedirs(user_dir, mode=0o750, exist_ok=False)
        subprocess.run(['chown', f'{sanitized_username}:{group_name}', user_dir], check=True, capture_output=True)
        logging.info(f"Directory {user_dir} created successfully for user {sanitized_username} with group {group_name}.")
    except FileExistsError:
        logging.error(f"The directory {user_dir} already exists.")
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while setting ownership: {e.stderr.decode().strip()}")

# Example usage:
# create_user_directory('newusername', 'users')

