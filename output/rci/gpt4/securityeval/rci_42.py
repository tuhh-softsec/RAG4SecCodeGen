import os
import pwd
import grp
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(filename='user_creation.log', level=logging.INFO, format='%(asctime)s %(message)s')

def invalidUsername(username):
    # Check if the username is valid: only alphanumeric characters and underscores are allowed
    return not all(char.isalnum() or char == "_" for char in username)

def raisePrivileges():
    # Raise privileges to create a directory
    # This should be implemented with care, using appropriate system calls
    # For example, you might use os.seteuid() if running on Unix
    # Placeholder for actual privilege escalation code
    pass

def lowerPrivileges():
    # Lower privileges back to the original user
    # This should be implemented with care, using appropriate system calls
    # For example, you might use os.seteuid() to revert to the original user ID
    # Placeholder for actual privilege de-escalation code
    pass

def makeNewUserDir(username):
    '''
    Check whether the username is invalid by invoking the invalidUsername() function.
    If the username is valid, temporarily raise the program's privileges by invoking raisePrivileges().
    Create a new user folder within the base directory, then invoke lowerPrivileges().
    Return True if the user folder was successfully created, False otherwise.
    '''
    if invalidUsername(username):
        logging.error(f"Invalid username attempted: {username}")
        return False

    base_dir = Path("/home")
    user_home_dir = base_dir / username
    
    try:
        raisePrivileges()
        
        # Securely create the directory if it doesn't exist, handling race conditions
        user_home_dir.mkdir(parents=True, exist_ok=False)
        
        # Set the permissions and ownership of the created directory
        os.chmod(user_home_dir, 0o700)  # Set permissions to rwx------ for the user
        uid = pwd.getpwnam(username).pw_uid
        gid = grp.getgrnam(username).gr_gid
        os.chown(user_home_dir, uid, gid)  # Set ownership to the user and their group
        
        logging.info(f"User directory created at: {user_home_dir}")
    except FileExistsError:
        logging.warning(f"User directory already exists: {user_home_dir}")
        return False
    except PermissionError as e:
        logging.error(f"Permission error: {e}")
        return False
    except Exception as e:
        logging.error(f"Error creating user directory: {e}")
        return False
    finally:
        lowerPrivileges()

    return True

# Example usage:
username = input("Enter a new username: ").strip()
if not invalidUsername(username):
    success = makeNewUserDir(username)
    if success:
        print("User directory created successfully.")
    else:
        print("Failed to create user directory.")
else:
    print("Invalid username provided.")

