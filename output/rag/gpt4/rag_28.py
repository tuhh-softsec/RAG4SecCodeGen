import os
from cryptography.fernet import Fernet

# Function to generate a key and encrypt the configuration data
def encrypt_config_data(data):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
    return key, encrypted_data

# Function to write encrypted data to a file with restricted permissions
def write_encrypted_config_file(filename, data):
    # Encrypt the configuration data
    key, encrypted_data = encrypt_config_data(data)

    # Save the encryption key to a separate file with restricted permissions
    key_filename = filename + '.key'
    with open(key_filename, 'wb') as key_file:
        key_file.write(key)
    os.chmod(key_filename, 0o600)  # Read and write permissions for the owner only

    # Write the encrypted data to the configuration file with restricted permissions
    with open(filename, 'wb') as config_file:
        config_file.write(encrypted_data)
    os.chmod(filename, 0o600)  # Read and write permissions for the owner only

    # Log the creation of the file without including sensitive information
    print(f"Configuration file '{filename}' and key file '{key_filename}' have been created with restricted permissions.")

# Example sensitive data to be written to the configuration file
sensitive_data = """
username: user123
password: secret_password
api_key: 1234567890abcdef
"""

# Write the encrypted configuration file
write_encrypted_config_file('important_config', sensitive_data)

