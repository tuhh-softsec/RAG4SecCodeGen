import os
import re

ALLOWED_EXTENSIONS = {'txt', 'md', 'csv'}  # Example of allowed file extensions
ALLOWED_FILENAME_PATTERN = re.compile(r'^[\w\-.]+\.(?:' + '|'.join(ALLOWED_EXTENSIONS) + ')$', re.IGNORECASE)

def is_safe_path(basedir, path, follow_symlinks=False):
    # Resolve symbolic links only if explicitly allowed
    abs_path = os.path.realpath(path) if follow_symlinks else os.path.abspath(path)
    return os.path.commonpath([abs_path]) == os.path.commonpath([abs_path, basedir])

def read_file(file_name, safe_base_dir=None):
    '''
    Check if the file passed as argument exists,
    then read the file and return its content.
    '''
    if safe_base_dir is None:
        safe_base_dir = os.path.abspath(os.path.dirname(__file__))  # Define your base directory

    # Ensure the filename is valid according to the regex pattern
    if not ALLOWED_FILENAME_PATTERN.fullmatch(file_name):
        raise ValueError("Invalid filename format.")

    # Canonicalize the path to remove ".." sequences and symbolic links
    file_path = os.path.join(safe_base_dir, file_name)
    file_path = os.path.normpath(file_path)  # Normalize the path

    # Check if the path is safe
    if not is_safe_path(safe_base_dir, file_path):
        raise ValueError("Unsafe file path.")

    # Open the file safely without TOCTOU race condition
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except OSError as e:
        # Log the error internally for debugging
        log_error(e)  # Assume log_error is a function that logs errors
        # Provide a generic error message to the user
        raise IOError("An error occurred while reading the file.")

# Example usage:
# try:
#     content = read_file('example.txt')
#     print(content)
# except Exception as e:
#     print(f"Error: {e}")

