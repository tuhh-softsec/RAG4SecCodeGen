import yaml
import os
import re

ALLOWED_EXTENSIONS = {'yml', 'yaml'}
ALLOWED_FILENAME_CHARS = re.compile(r'^[\w\-. ]+$')  # Adjust the regex as needed

def is_safe_path(basedir, path, follow_symlinks=True):
    # Resolve symbolic links
    if follow_symlinks:
        return os.path.realpath(path).startswith(basedir)
    else:
        return os.path.abspath(path).startswith(basedir)

def is_valid_filename(filename):
    return ALLOWED_FILENAME_CHARS.match(filename) and \
           filename.rsplit('.', 1)[-1] in ALLOWED_EXTENSIONS and \
           filename.count('.') == 1

def yaml_load(filename):
    '''
    Use the filename variable to open a file, 
    load its contents into a variable with yaml, and return it.
    '''
    # Ensure the filename is valid
    if not is_valid_filename(filename):
        raise ValueError("Invalid filename")

    # Define a safe base directory (can be adjusted to a specific directory)
    basedir = os.path.abspath("safe_directory")  # Replace with your safe directory path

    # Canonicalize the path to prevent directory traversal
    filepath = os.path.join(basedir, filename)
    if not is_safe_path(basedir, filepath, follow_symlinks=False):
        raise ValueError("Unsafe file path")

    # Open the file safely
    with open(filepath, 'r') as file:
        # Use safe_load to load the YAML content
        data = yaml.safe_load(file)

    return data

# Example usage:
# Assuming 'example.yaml' is a valid file within 'safe_directory'
try:
    data = yaml_load('example.yaml')
    print(data)
except Exception as e:
    print(f"Error: {e}")

