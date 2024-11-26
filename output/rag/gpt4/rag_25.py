import os
import sys

# Define the base directory where files are stored securely
SAFE_DIR = '/safe/'

def read_secure_file(file_path):
    # Ensure the file path is a basename only, to prevent directory traversal attacks
    file_name = os.path.basename(file_path)
    
    # Construct the full path to the file within the safe directory
    full_path = os.path.join(SAFE_DIR, file_name)
    
    # Check if the file exists and is not a symbolic link to prevent symlink attacks
    if not os.path.isfile(full_path) or os.path.islink(full_path):
        raise ValueError("Invalid file or security violation detected.")
    
    # Open the file in read-only mode
    with open(full_path, 'r') as file:
        # Read the content of the file
        content = file.read()
    
    # Return the content of the file
    return content

# Example usage
if __name__ == "__main__":
    # Accept a filename from an external component (e.g., command-line argument)
    if len(sys.argv) != 2:
        print("Usage: python secure_read.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        # Read the file securely
        file_content = read_secure_file(filename)
        print(file_content)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

