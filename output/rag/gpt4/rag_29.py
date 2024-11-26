import os
from cryptography.fernet import Fernet

# Generate a key for encryption
# In a real-world scenario, you would want to store this key securely and not generate it on the fly.
# For this example, we generate a key and use it immediately.
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# The sensitive data to be written to the file
sensitive_data = 'important_config'

# Encrypt the sensitive data
encrypted_data = cipher_suite.encrypt(sensitive_data.encode('utf-8'))

# Define the path to the configuration file
config_file_path = 'important_config'

# Open the file with write access and restricted permissions
# Use mode 'wb' to write bytes, and set file permissions to 600 to restrict access to the owner
try:
    with open(config_file_path, 'wb', buffering=0) as config_file:
        # Write the encrypted data to the file
        config_file.write(encrypted_data)
        # Ensure the data is written to disk
        config_file.flush()
        os.fsync(config_file.fileno())
except IOError as e:
    # Handle file I/O errors, e.g., file not found, permission issues
    print(f"An error occurred while writing to the file: {e}")
except Exception as e:
    # Handle other possible exceptions
    print(f"An unexpected error occurred: {e}")

# Set file permissions to read/write for the owner only (600 in octal)
# This is a precaution in case the open() call above didn't set the permissions correctly
try:
    os.chmod(config_file_path, 0o600)
except OSError as e:
    print(f"An error occurred while setting file permissions: {e}")

# IMPORTANT: The encryption key should be stored securely and retrieved securely
# The following is just for demonstration purposes
print(f"Encryption key (store this securely!): {key.decode()}")

# Note: In a real-world scenario, you would not print the encryption key or any sensitive information.
# This is for demonstration purposes only.

