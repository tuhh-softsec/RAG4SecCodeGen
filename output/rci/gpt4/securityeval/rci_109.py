import os
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_executable_file(data, directory):
    '''
    Create a unique binary file and make it executable in a secure manner.
    '''
    if not os.path.isdir(directory) or not os.access(directory, os.W_OK):
        raise ValueError("Provided directory is not writable or does not exist.")

    mode = 0o700  # Restrict permissions to the file owner only
    filepath = None

    try:
        # Generate a unique filename with restricted permissions from the outset
        fd, filepath = tempfile.mkstemp(suffix='.bim', dir=directory, mode=mode)
        os.close(fd)  # Close the file descriptor as we will open the file again later

        # Write binary data to the file
        with open(filepath, 'wb') as file:
            file.write(data)

        # Make the file executable (redundant if mode is set correctly, but included for clarity)
        os.chmod(filepath, mode)
        logging.info(f"File '{os.path.basename(filepath)}' has been created and made executable.")

        return filepath  # Return the path to the created file for further use or cleanup

    except (IOError, PermissionError, OSError) as e:
        logging.error(f"An error occurred: {e}")
        if filepath and os.path.exists(filepath):
            os.unlink(filepath)  # Clean up by removing the file if an error occurs
        raise

    finally:
        # Additional cleanup logic if needed
        pass

# Example usage:
binary_data = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09'  # Dummy binary data

# Specify a secure directory where the file should be created
secure_directory = '/path/to/secure/directory'
if not os.path.exists(secure_directory):
    os.makedirs(secure_directory, mode=0o700)

try:
    filepath = create_executable_file(binary_data, directory=secure_directory)
    # Use the file as needed
finally:
    # Remember to remove the executable file when it is no longer needed
    if filepath and os.path.exists(filepath):
        os.unlink(filepath)

# Note: Ensure that the directory specified is secure and that the script runs with minimal necessary privileges.

