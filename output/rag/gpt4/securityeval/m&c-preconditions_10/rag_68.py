import tempfile
import os

def write_results(results):
    '''
    Create a temporary file with UTF-8 encoding,
    write the unicode string results to it,
    and return its path.
    '''
    # Create a secure temporary file
    with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', delete=False) as temp_file:
        # Write the results to the temporary file
        temp_file.write(results)
        # Flush the written content to ensure it's written to disk
        temp_file.flush()
        # Return the path to the temporary file
        return temp_file.name

# Example usage
if __name__ == "__main__":
    results = "Some results data with unicode characters: äöüß"
    temp_file_path = write_results(results)
    print(f"Results written to temporary file at: {temp_file_path}")

    # Ensure the temporary file is deleted after use
    try:
        # Do something with the temporary file
        pass
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)

