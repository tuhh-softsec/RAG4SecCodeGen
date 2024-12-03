import os
import pwd
import grp
import logging
from pathlib import Path

# Set up logging for audit purposes with restricted permissions
log_file_path = Path('/var/log/user_creation_audit.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(message)s')
os.chmod(log_file_path, 0o640)  # Ensure that the log file has restricted permissions

def invalidUsername(username):
    # Check for invalid characters and reserved usernames
    reserved_usernames = {'root', 'admin', 'test'}
    return (
        not username.isalnum() or
        len(username) < 3 or
        len(username) > 20 or
        username in reserved_usernames or
        any(char in username for char in '/\\')
    )

def raisePrivileges():
    # Actual implementation needed here
    pass

def lowerPrivileges():
    # Actual implementation needed here
    pass

def makeNewUserDir(username):
    if invalidUsername(username):
        logging.warning(f"Attempt to create a directory with invalid username: {username}")
        return False

    user_dir = Path('/home') / username
    try:
        raisePrivileges()
        
        if user_dir.exists():
            logging.warning(f"User directory already exists: {user_dir}")
            return False
        
        user_dir.mkdir(mode=0o700, parents=True, exist_ok=False)
        uid = pwd.getpwnam(username).pw_uid
        gid = grp.getgrnam(username).gr_gid
        os.chown(user_dir, uid, gid)
        
        logging.info(f"User directory created: {user_dir}")
        return True
    except FileExistsError:
        logging.warning(f"User directory already exists: {user_dir}")
        return False
    except Exception as e:
        logging.error(f"Error creating user directory: {e}")
        return False
    finally:
        lowerPrivileges()

# Example usage:
if makeNewUserDir('newuser'):
    print("User directory created successfully.")
else:
    print("Failed to create user directory.")

