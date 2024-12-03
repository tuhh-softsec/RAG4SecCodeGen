import tempfile
import os
import logging

# Configure logging to handle different levels and direct messages to a secure location
logging.basicConfig(level=logging.ERROR, filename='error.log')

def write_results(results):
    '''
    Create a temporary file with UTF-8 encoding,
    write the unicode string results to it,
    and handle the file securely.
    '''
    # Create a temporary file securely with restrictive permissions from the start
    fd, temp_file_path = tempfile.mkstemp(mode='w', encoding='utf-8')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as temp_file:
            # Write the results to the temporary file
            temp_file.write(results)
            temp_file.flush()
            os.fsync(temp_file.fileno())
    except IOError as e:
        # Handle specific file I/O exceptions
        logging.error(f"An I/O error occurred: {e}")
        raise
    except Exception as e:
        # Handle other possible exceptions
        logging.error(f"An unexpected error occurred: {e}")
        raise
    finally:
        # Securely delete the file
        try:
            # Overwrite the file with zeros or use a secure deletion method before removing
            with open(temp_file_path, 'wb') as f:
                f.write(b'\x00' * os.path.getsize(temp_file_path))
            os.remove(temp_file_path)
        except OSError as e:
            # Handle specific OS exceptions during file deletion
            logging.error(f"Failed to delete temporary file: {e}")
            raise

# Example usage:
results_data = "Some unicode data with special characters: äöüß"
try:
    write_results(results_data)
except Exception as e:
    logging.error(f"An error occurred during the write operation: {e}")

