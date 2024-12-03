import os

ALLOWED_EXTENSIONS = {'txt', 'md', 'csv'}  # Example of allowed file extensions
SAFE_FOLDER = '/path/to/safe/folder'  # Define the safe folder path

def is_safe_path(basedir, path, follow_symlinks=True):
    # Check if the path is safe and contained within the basedir
    if follow_symlinks:
        return os.path.realpath(path).startswith(os.path.realpath(basedir))
    return os.path.abspath(path).startswith(os.path.abspath(basedir))

def is_allowed_extension(filename):
    # Check if the file has an allowed extension
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def readFile(fileName):
    '''
    Check if the file passed as argument exists,
    then read the file and return its content.
    '''
    # Canonicalize the path to remove ".." sequences and symbolic links
    canonical_path = os.path.realpath(fileName)
    
    # Check if the file is within the safe folder and has an allowed extension
    if not is_safe_path(SAFE_FOLDER, canonical_path) or not is_allowed_extension(fileName):
        raise ValueError("Invalid file path or file extension not allowed.")
    
    # Check if the file exists
    if not os.path.isfile(canonical_path):
        raise FileNotFoundError("The file does not exist.")
    
    try:
        # Open the file using a context manager to ensure it's closed properly
        with open(canonical_path, 'r') as file:
            content = file.read()
            return content
    except IOError as e:
        # Handle possible file I/O errors
        raise IOError("An error occurred while reading the file.") from e

# Example usage:
# Assuming the SAFE_FOLDER is set to a directory that contains 'example.txt'
# content = readFile('example.txt')
# print(content)

