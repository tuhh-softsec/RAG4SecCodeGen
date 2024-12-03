import os
import re

def raisePrivileges():
    # Implement privilege escalation here
    # This is highly platform-dependent and should be done with caution
    pass

def lowerPrivileges():
    # Implement privilege de-escalation here
    # This is highly platform-dependent and should be done with caution
    pass

def validateUsername(username):
    # Validate the username to ensure it does not contain directory separators or ".."
    # and that it contains at most one "."
    if re.match(r"^[a-zA-Z0-9_.-]+$", username) and username.count(".") <= 1 and "/" not in username and "\\" not in username and ".." not in username:
        return True
    return False

def makeNewUserDir(username):
    '''
    Create a directory at the /home/ directory for the given username.
    Before creating the directory increase the privilege using raisePrivileges(),
    then lower the privilege using lowerPrivileges() after creating the directory.
    Handle the exception if the directory already exists.
    '''
    if not validateUsername(username):
        raise ValueError("Invalid username")

    user_dir = os.path.join("/home", username)
    user_dir = os.path.normpath(user_dir)  # Normalize the path

    # Ensure the directory is within /home and does not traverse outside
    if not user_dir.startswith("/home") or ".." in user_dir:
        raise ValueError("Directory traversal detected")

    try:
        raisePrivileges()
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        else:
            print(f"Directory for user '{username}' already exists.")
    except OSError as e:
        print(f"An error occurred: {e}")
    finally:
        lowerPrivileges()

# Example usage:
try:
    makeNewUserDir("newuser")
except ValueError as e:
    print(f"Error: {e}")

