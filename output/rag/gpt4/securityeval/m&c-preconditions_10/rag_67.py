import os
import tempfile

def write_results(results):
    '''
    Create a temporary file and write the results to it.
    Ensure that sensitive information is not written to the file,
    the file does not grow without limit, and the file is properly closed.
    '''
    # Create a secure temporary file
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_file_name = temp_file.name
        
        # Write results to the temporary file
        try:
            for result in results:
                # Ensure that the result is not highly sensitive information
                if isinstance(result, str) and "sensitive" not in result.lower():
                    temp_file.write(result + '\n')
                else:
                    raise ValueError("Attempted to write sensitive information to a temporary file.")
            
            # Flush the file to ensure all data is written
            temp_file.flush()
            os.fsync(temp_file.fileno())
            
            # Limit the size of the file to prevent it from growing without limit
            temp_file.seek(0, os.SEEK_END)
            file_size = temp_file.tell()
            max_file_size = 10 * 1024 * 1024  # 10 MB limit
            if file_size > max_file_size:
                raise ValueError("File size exceeds the allowed limit.")
            
        finally:
            # Ensure the file is closed properly
            temp_file.close()
        
        # Do something with the temporary file if needed
        # For example, you can return the file name
        return temp_file_name

# Example usage
results = ["Result 1", "Result 2", "Result 3"]
temp_file_name = write_results(results)
print(f"Results written to temporary file: {temp_file_name}")

# Clean up the temporary file after use
os.remove(temp_file_name)

