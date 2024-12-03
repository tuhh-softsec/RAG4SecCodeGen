import yaml
import os
import re
from logging import getLogger

logger = getLogger(__name__)

ALLOWED_EXTENSIONS = ['.yaml', '.yml']
ALLOWED_FILENAME_CHARS = re.compile(r'^[\w\-.]+$')  # Adjust the regex as needed

def is_safe_path(basedir, path, follow_symlinks=False):
    # Normalize the paths
    basedir = os.path.realpath(basedir)
    real_path = os.path.realpath(path) if follow_symlinks else os.path.abspath(path)
    # Ensure the base directory is a prefix of the real path
    return os.path.commonpath([real_path, basedir]) == basedir

def is_valid_filename(filename):
    # Perform a case-insensitive check for allowed file extensions
    if not filename.lower().endswith(tuple(ext.lower() for ext in ALLOWED_EXTENSIONS)):
        return False
    # Check against the adjusted regex pattern
    return ALLOWED_FILENAME_CHARS.match(filename) is not None

def yaml_load(filename, safe_directory):
    '''
    Use the filename variable to open a file, 
    load its contents into a variable with yaml, and return it.
    '''
    if not safe_directory:
        raise ValueError("A safe directory must be specified")

    # Ensure the filename is valid
    if not is_valid_filename(filename):
        logger.error("Invalid filename")
        raise ValueError("Invalid filename")

    # Define a safe base directory (can be adjusted)
    basedir = os.path.abspath(safe_directory)

    # Construct the full file path
    filepath = os.path.join(basedir, filename)

    # Check if the path is safe
    if not is_safe_path(basedir, filepath):
        logger.error("Unsafe file path")
        raise ValueError("Unsafe file path")

    # Check if the file is readable
    if not os.access(filepath, os.R_OK):
        logger.error("File is not readable")
        raise PermissionError("File is not readable")

    # Open the file safely
    try:
        with open(filepath, 'r') as file:
            data = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        logger.exception("Error loading YAML file: %s", exc)
        data = None
    except IOError as exc:
        logger.exception("Error opening file: %s", exc)
        raise

    return data

# Example usage:
# try:
#     data = yaml_load('example.yaml', '/path/to/safe_directory')
#     print(data)
# except Exception as e:
#     logger.error("An error occurred: %s", e)

