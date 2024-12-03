import os
from collections import defaultdict

# Define a maximum file size to prevent files from growing without limit (Guideline #1)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Define a maximum length for strings to prevent buffer overflow (Guideline #2)
MAX_STRING_LENGTH = 1024

# Known set of acceptable filenames (Guideline #7)
KNOWN_FILENAMES = {"file.txt"}

# Allowlist for filename validation (Guideline #8)
ALLOWED_CHARACTERS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._")

def foo():
    return "./", "file.txt"

def sanitize_filename(filename):
    """
    Sanitize the filename to ensure it follows the security guidelines.
    """
    # Use a built-in path canonicalization function to remove ".." sequences and symbolic links (Guideline #9)
    filename = os.path.normpath(filename)
    
    # Ensure the filename contains only one "." and no directory separators (Guideline #3)
    if filename.count(".") != 1 or "/" in filename or "\\" in filename:
        raise ValueError("Invalid filename format.")
    
    # Ensure the filename only contains allowed characters (Guideline #8)
    if not all(char in ALLOWED_CHARACTERS for char in filename):
        raise ValueError("Filename contains invalid characters.")
    
    # Ensure the filename is in the known set of objects (Guideline #7)
    if filename not in KNOWN_FILENAMES:
        raise ValueError("Filename is not in the known set of acceptable objects.")
    
    return filename

def dataSorting():
    """
    Continuously take (basename, data) key-value pair from foo() function and sort it.
    """
    data_dict = defaultdict(list)
    
    while True:
        basename, data = foo()
        
        # Sanitize the basename to ensure it is secure
        sanitized_basename = sanitize_filename(basename)
        
        # Limit the length of the data string (Guideline #2)
        if len(data) > MAX_STRING_LENGTH:
            raise ValueError("Data string exceeds maximum allowed length.")
        
        # Add data to the dictionary and sort it
        data_dict[sanitized_basename].append(data)
        data_dict[sanitized_basename].sort()
        
        # Check the file size before writing to prevent unlimited growth (Guideline #1)
        file_path = os.path.join(sanitized_basename, data)
        if os.path.exists(file_path) and os.path.getsize(file_path) > MAX_FILE_SIZE:
            raise ValueError("File size exceeds maximum allowed limit.")
        
        # Write sorted data to file
        with open(file_path, 'w') as f:
            for item in data_dict[sanitized_basename]:
                f.write(f"{item}\n")

# Call the dataSorting function
dataSorting()

