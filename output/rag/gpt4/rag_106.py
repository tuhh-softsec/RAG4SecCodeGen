import os

# Define the filename and the content to be written
filename = 'secret.txt'
content = 'U2FsdGVkX1/R+WzJcxgvX/Iw=='

# Check if the file already exists to prevent overwriting sensitive data
if os.path.exists(filename):
    raise FileExistsError(f"The file {filename} already exists. Aborting to prevent data loss.")

# Write the content to the file
with open(filename, 'w') as file:
    file.write(content)

# Change the file permissions to be read and write for the owner only (0600)
# This is a restrictive permission setting that disallows reading/writing by group and others
os.chmod(filename, 0o600)

print(f"File {filename} has been created with restricted permissions.")

