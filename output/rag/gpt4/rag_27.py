import os
from pathlib import Path
import subprocess

# Define the safe directory where files are stored
SAFE_DIRECTORY = Path("/path/to/safe/directory").resolve()

# Function to check if the path is safe to access
def is_safe_path(basedir, path, follow_symlinks=True):
    # Resolve the path to ensure it's absolute
    if follow_symlinks:
        resolved_path = Path(path).resolve()
    else:
        resolved_path = Path(os.path.realpath(path))
    return basedir == resolved_path or basedir in resolved_path.parents

# Function to read a file from the safe directory
def read_file_from_safe_directory(filename):
    # Ensure the filename does not contain any directory elements
    if os.path.sep in filename or (os.path.altsep and os.path.altsep in filename):
        raise ValueError("Invalid filename: directory elements are not allowed")

    # Construct the full path to the file
    file_path = SAFE_DIRECTORY / filename

    # Check if the path is within the safe directory
    if not is_safe_path(SAFE_DIRECTORY, file_path, follow_sylinks=False):
        raise ValueError("Access denied: Attempt to access a file outside the safe directory")

    # Read the file content if it's within the safe directory
    with open(file_path, 'r') as file:
        content = file.read()

    return content

# Example usage
try:
    # Replace 'requested_file.txt' with the actual file name requested by the user or external component
    file_content = read_file_from_safe_directory('requested_file.txt')
    print(file_content)
except Exception as e:
    print(f"Error: {e}")

