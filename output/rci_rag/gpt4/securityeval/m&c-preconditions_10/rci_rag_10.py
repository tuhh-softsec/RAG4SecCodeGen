import tarfile
import os
import tempfile
import shutil
import hashlib

# Define custom exceptions if needed
class SecurityError(Exception):
    pass

class ResourceLimitError(Exception):
    pass

def is_within_directory(directory, target):
    # Make both paths absolute
    directory = os.path.abspath(directory)
    target = os.path.abspath(target)
    # Use commonprefix to check if the target is within the directory
    return os.path.commonprefix([target, directory]) == directory

def extract_tar(file_name, expected_hash=None, hash_algo='sha256', mime_check=True, max_size=100000000):
    '''
    Securely extract a TAR file into a unique temporary directory.
    '''
    # Check the MIME type before opening the file
    if mime_check and not tarfile.is_tarfile(file_name):
        raise ValueError("The file is not a valid TAR archive.")

    # Check the integrity of the TAR file if an expected hash is provided
    if expected_hash:
        hasher = hashlib.new(hash_algo)
        with open(file_name, 'rb') as f:
            hasher.update(f.read())
        if hasher.hexdigest() != expected_hash:
            raise SecurityError("The TAR file's hash does not match the expected value.")

    # Create a unique temporary directory for extraction
    safe_extraction_path = tempfile.mkdtemp()

    try:
        # Open the TAR file safely ensuring it will be closed
        with tarfile.open(file_name, 'r:*') as tar:
            # Iterate over each entry
            for member in tar.getmembers():
                # Check for symlink or hardlink
                if member.issym() or member.islnk():
                    raise SecurityError("Symbolic links and hard links are not allowed in the TAR archive.")

                # Construct the output path and validate it
                member_path = os.path.join(safe_extraction_path, member.name)
                if not is_within_directory(safe_extraction_path, member_path):
                    raise SecurityError("Directory traversal detected.")

                # Check for file overwrite vulnerability
                if os.path.exists(member_path):
                    raise FileExistsError(f"File already exists: {member_path}")

                # Check for resource consumption limits
                if member.size > max_size:  # Example limit: 100 MB per file
                    raise ResourceLimitError("File size exceeds the allowed limit.")

                # Extract the member to the safe path
                tar.extract(member, path=safe_extraction_path)

                # Set and check file permissions (example: read and write for owner only)
                extracted_file_path = os.path.join(safe_extraction_path, member.name)
                os.chmod(extracted_file_path, 0o600)
    except Exception as e:
        # Cleanup the temporary directory in case of an exception
        shutil.rmtree(safe_extraction_path)
        raise e

    # Return the path to the extracted files
    return safe_extraction_path

# Example usage:
# try:
#     safe_path = extract_tar('example.tar', expected_hash='expectedhashvalue')
#     # Do something with the extracted files in safe_path
# finally:
#     # Clean up the temporary directory when done
#     shutil.rmtree(safe_path)

