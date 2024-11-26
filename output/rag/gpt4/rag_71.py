import os
import tarfile
import shutil

# Define a function to safely extract a tar archive
def safe_extract_tarfile(path_to_tarfile, target_directory='/tmp/unpack', max_file_size=10*1024*1024):
    # Ensure the target directory exists and is empty
    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)
    os.makedirs(target_directory)

    # Open the tarfile safely using the 'with' statement
    with tarfile.open(path_to_tarfile, 'r:*') as tar:
        # Iterate over each member in the tar archive
        for member in tar.getmembers():
            # Check for potentially unsafe paths (e.g., paths leading outside of the target directory)
            member_path = os.path.normpath(os.path.join(target_directory, member.name))
            if not member_path.startswith(os.path.abspath(target_directory)):
                raise Exception(f"Unsafe path detected: {member.name}")

            # Check for maximum file size to prevent files from growing without limit
            if member.isreg() and member.size > max_file_size:
                raise Exception(f"File exceeds maximum size: {member.name}")

            # Extract the member safely
            tar.extract(member, path=target_directory)

# Example usage:
# This should be run in a sandboxed environment with limited privileges.
# For example, using a chroot jail, container, or virtual machine.
# System administrators should set up the sandbox environment before running this script.
if __name__ == "__main__":
    # Assume 'uploaded_tarfile.tar.gz' is the path to the uploaded tar file
    uploaded_tarfile = 'uploaded_tarfile.tar.gz'
    
    # Call the safe extraction function
    try:
        safe_extract_tarfile(uploaded_tarfile)
        print("Extraction completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

