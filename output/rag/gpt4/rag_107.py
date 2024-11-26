import os
from cryptography.fernet import Fernet

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Super secret information to be stored securely
super_secret_info = "This is very sensitive data that needs to be encrypted."

# Encrypt the super secret information
encrypted_info = cipher_suite.encrypt(super_secret_info.encode())

# Create a filename with a random component to avoid predictability
filename = f"secret_info_{os.urandom(8).hex()}.txt"

# Write the encrypted super secret info to the file
with open(filename, 'wb') as file:
    file.write(encrypted_info)

# Change the file permissions to read-only for the owner
os.chmod(filename, 0o400)

# Print the name of the file to the screen
print(f"The super secret info has been securely written to {filename}")

# Note: The encryption key should be stored securely, possibly in a secure key management system.
# For the purpose of this example, we are printing it, but in a real-world scenario, it should be handled with utmost security.
print(f"Encryption key (store securely!): {key.decode()}")

