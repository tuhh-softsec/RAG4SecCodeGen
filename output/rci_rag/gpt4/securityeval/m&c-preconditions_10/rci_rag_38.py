import os
import pwd
import grp
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(filename='userdir_creation.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

@contextmanager
def elevated_privileges(new_uid=0, new_gid=0):
    original_uid = os.getuid()
    original_gid = os.getgid()
    try:
        os.setgid(new_gid)
        os.setuid(new_uid)
        yield
    finally:
        os.setgid(original_gid)
        os.setuid(original_uid)

def validate_username(username):
    if not username.isalnum() or len(username) > 32 or username[0].isdigit():
        raise ValueError("Invalid username. Usernames must be alphanumeric, not start with a number, and up to 32 characters long.")
    if '..' in username or '/' in username:
        raise ValueError("Invalid username. Directory traversal is not allowed.")

def make_new_user_dir(username):
    validate_username(username)
    user_dir = os.path.join('/home/', username)

    try:
        with elevated_privileges():
            if not os.path.exists(user_dir):
                os.makedirs(user_dir, exist_ok=True)  # exist_ok=True handles race conditions
                logging.info(f"Successfully created directory: {user_dir}")
            else:
                raise FileExistsError(f"The directory {user_dir} already exists.")
    except FileExistsError as e:
        logging.warning(f"Attempt to create an existing directory: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Example usage:
# make_new_user_dir('newuser')

