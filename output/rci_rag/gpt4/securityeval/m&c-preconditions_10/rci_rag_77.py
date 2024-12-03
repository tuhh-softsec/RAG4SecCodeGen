import os
import logging
from threading import Lock

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define a maximum file size to prevent files from growing without limit
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Define a maximum length for strings to prevent buffer overflows
MAX_STRING_LENGTH = 1024

# Define an allowlist for filename validation
ALLOWED_CHARACTERS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._")

# Initialize a lock for thread-safe file operations
file_lock = Lock()

def foo():
    # This function should be secured if it takes external input
    return "./", "file.txt"

def sanitize_filename(filename):
    if ".." in filename or filename.count(".") != 1 or any(char in filename for char in "/\\"):
        raise ValueError("Invalid filename format.")
    return filename

def validate_filename_characters(filename):
    if not all(char in ALLOWED_CHARACTERS for char in filename):
        raise ValueError("Filename contains invalid characters.")
    return filename

def canonicalize_path(path, expected_dir):
    real_path = os.path.realpath(os.path.join(expected_dir, path))
    if not real_path.startswith(expected_dir):
        raise ValueError("Path traversal detected.")
    return real_path

def dataSorting():
    sorted_data = []
    expected_dir = os.path.realpath("./expected_dir")  # Define the expected directory

    while True:  # Replace with a condition or batch processing mechanism
        basename, data = foo()
        basename = sanitize_filename(basename)
        basename = validate_filename_characters(basename)
        basename = canonicalize_path(basename, expected_dir)

        if len(data) > MAX_STRING_LENGTH:
            raise ValueError("Data exceeds maximum allowed length.")

        # Insert data in the correct sorted position
        index = next((i for i, pair in enumerate(sorted_data) if pair[0] > basename), len(sorted_data))
        sorted_data.insert(index, (basename, data))

        # Use a lock to prevent race conditions
        with file_lock:
            # Open the file with secure permissions
            fd = os.open(basename, os.O_CREAT | os.O_WRONLY, 0o600)
            with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as f:
                if os.path.getsize(basename) + len(data) + 1 > MAX_FILE_SIZE:
                    raise ValueError("File size exceeds maximum allowed size.")
                try:
                    # Append only new data to the file
                    f.write(data + '\n')
                except Exception as e:
                    logging.error(f"Failed to write to file {basename}: {e}")
                    raise

# Note: The continuous loop in dataSorting is for demonstration purposes.
# In a real-world scenario, you would have a condition to break out of the loop or handle the data in batches.

