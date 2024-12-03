import os
import tarfile

def extract_tar(file_name):
    '''
    Open a TAR file, 
    iterate over each entry, 
    and extract its contents in the /tmp/ directory
    '''
    # Define the safe extraction directory
    safe_extraction_dir = '/tmp/'

    # Ensure the safe_extraction_dir is an absolute path
    safe_extraction_dir = os.path.abspath(safe_extraction_dir)

    # Open the TAR file safely using a context manager to ensure it's closed properly
    with tarfile.open(file_name, 'r:*') as tar:
        # Iterate over each member
        for member in tar.getmembers():
            # Construct the full path to the extraction location
            member_path = os.path.join(safe_extraction_dir, member.name)

            # Normalize the path to prevent directory traversal attacks
            safe_member_path = os.path.normpath(member_path)

            # Ensure the path starts with the safe_extraction_dir and does not contain ".."
            if not safe_member_path.startswith(safe_extraction_dir) or '..' in safe_member_path:
                raise Exception(f"Unsafe path detected: {safe_member_path}")

            # Extract the member to the safe path
            tar.extract(member, safe_extraction_dir)

# Example usage:
# extract_tar('example.tar')

