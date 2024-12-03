import tempfile
import os
import stat
import shutil

def secure_delete(file_path, passes=3):
    '''
    Overwrite the file with random data and then delete it.
    '''
    if os.path.exists(file_path):
        with open(file_path, "ba+" if os.name == 'nt' else "bw+") as f:
            length = f.tell()
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(length))
        os.remove(file_path)

def write_results(results):
    '''
    Create a temporary file with UTF-8 encoding,
    write the unicode string results to it,
    and securely delete the file after use.
    '''
    # Use a context manager to ensure the file is closed properly
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as temp_file:
        temp_file.write(results)
        # Get the path of the temporary file
        temp_path = temp_file.name
        # Set restrictive permissions on the file (read and write for owner only)
        os.chmod(temp_path, stat.S_IRUSR | stat.S_IWUSR)

    # Perform necessary operations on the file within this function or within a controlled environment
    # Example of secure file handling without exposing the path
    # Read the file content for demonstration purposes (replace with actual use case)
    with open(temp_path, 'r', encoding='utf-8') as temp_file:
        file_content = temp_file.read()
        # Ensure sensitive data is not printed or logged in an insecure manner
        # print("Results read from temporary file (not shown to the user).")

    # Securely delete the file
    try:
        secure_delete(temp_path)
    except OSError as e:
        # Depending on the context, log the error to a secure log file or alert an administrator
        # For example, log the error (logging not shown here)
        print(f"Error: {e.strerror}. File {temp_path} was not securely deleted.")

# Example usage
if __name__ == "__main__":
    results = "Some results data with unicode characters: äöüß"
    write_results(results)
    # The path of the temporary file is not exposed to the user or logs

