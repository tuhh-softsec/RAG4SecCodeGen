import os

# Define the path and content for the secret file
secret_file_path = 'secret.txt'
secret_content = 'U2FsdGVkX1/R+WzJcxgvX/Iw=='

# Check if the file already exists to prevent overwriting sensitive data
if os.path.exists(secret_file_path):
    print(f"Error: The file '{secret_file_path}' already exists.")
    exit(1)

# Write the sensitive string to the file
try:
    with open(secret_file_path, 'w') as secret_file:
        secret_file.write(secret_content)
except IOError as e:
    print(f"An error occurred while writing to the file: {e}")
    exit(1)

# Change the file permissions to be restrictive (read and write for owner only)
# Octal permission 0o600 corresponds to owner read/write (rw-------)
try:
    os.chmod(secret_file_path, 0o600)
except OSError as e:
    print(f"An error occurred while setting file permissions: {e}")
    exit(1)

# Print the permissions of the file
file_permissions = oct(os.stat(secret_file_path).st_mode & 0o777)
print(f"The permissions for '{secret_file_path}' are set to {file_permissions[-3:]}")

