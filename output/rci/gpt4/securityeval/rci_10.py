import tarfile
import os
import tempfile
import shutil

def is_within_directory(directory, target):
    '''
    Ensure that the target path is within the directory.
    '''
    # Resolve any symbolic links and relative paths
    directory = os.path.realpath(directory)
    target = os.path.realpath(target)

    # Use commonpath to check if the target is within the directory
    return os.path.commonpath([target, directory]) == directory

def extract_tar(file_name):
    '''
    Open a TAR file, 
    iterate over each entry, 
    and extract its contents in a secure temporary directory.
    '''
    # Create a unique temporary directory for extraction
    with tempfile.TemporaryDirectory() as extract_to:
        # Open the TAR file safely with 'r:*' to read with transparent compression
        with tarfile.open(file_name, 'r:*') as tar:
            # Check for archive bombs by setting limits on the number of files and their sizes
            max_files = 1000
            max_size = 100 * 1024 * 1024  # 100 MB
            total_files = 0
            total_size = 0

            # Iterate over each member
            for member in tar.getmembers():
                # Skip symlinks or other potentially dangerous file types
                if member.islnk() or member.issym():
                    continue

                # Check for hard links that might point outside the extraction directory
                if member.islnk():
                    link_target = os.path.join(extract_to, member.linkname)
                    if not is_within_directory(extract_to, link_target):
                        print(f"Skipping hard link to outside of extraction directory: {member.name}")
                        continue

                # Normalize member name to prevent directory traversal
                member_path = os.path.normpath(os.path.join(extract_to, member.name))
                if not is_within_directory(extract_to, member_path):
                    print(f"Attempted Path Traversal in TAR file: {member.name}")
                    continue

                # Check for file name collisions
                if os.path.exists(member_path):
                    print(f"Skipping existing file: {member.name}")
                    continue

                # Check for archive bombs
                total_files += 1
                total_size += member.size
                if total_files > max_files or total_size > max_size:
                    raise Exception("TAR file is too large or contains too many files.")

                # Extract the member safely
                tar.extract(member, path=extract_to)

                # Set safe permissions (e.g., 600 for files, 700 for directories)
                if member.isdir():
                    os.chmod(member_path, 0o700)
                else:
                    os.chmod(member_path, 0o600)

        # At this point, all files have been extracted safely and can be used
        # Perform any necessary operations on the extracted files here

        # When done, the temporary directory and its contents will be cleaned up automatically

# Example usage:
# extract_tar('example.tar')

