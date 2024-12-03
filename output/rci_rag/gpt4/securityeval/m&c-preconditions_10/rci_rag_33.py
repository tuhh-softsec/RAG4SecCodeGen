from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import secrets
import logging
import os

# Configure logging appropriately for your application
logging.basicConfig(level=logging.INFO)

def encrypt_data(data, key):
    '''
    Encrypt data using AES in CBC mode with a secure random IV.
    The key must be of a valid length for AES (16, 24, 32 bytes).
    The IV is prepended to the encrypted data for use in decryption.
    '''
    # Validate key length
    if len(key) not in (16, 24, 32):
        raise ValueError("Invalid key size")

    # Generate a random initialization vector (IV) for CBC mode
    iv = get_random_bytes(AES.block_size)

    # Create an AES cipher object with the key and IV in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Pad the data to be a multiple of the block size
    padded_data = pad(data, AES.block_size)

    # Encrypt the data
    try:
        encrypted_data = cipher.encrypt(padded_data)
    except ValueError as e:
        # Log the exception without exposing sensitive information
        logging.error(f"Encryption failed: {e}")
        return None

    # Return the IV and encrypted data together
    return iv + encrypted_data

# Example usage:
# Securely generate a random key (placeholder for a key management solution)
key = secrets.token_bytes(32)  # AES-256

# Your data to encrypt
data_to_encrypt = b"Sensitive data that needs to be encrypted"

# Encrypt the data
encrypted_data = encrypt_data(data_to_encrypt, key)
if encrypted_data is not None:
    # At this point, you would store or transmit `encrypted_data` securely.
    # Remember not to store the key alongside the encrypted data.
    # Ensure secure transmission (e.g., via TLS/SSL) and secure storage of the key.
    # Consider using a key vault or HSM for key management in a production environment.
    pass
else:
    # Handle encryption failure
    pass

# Additional security considerations:
# - Implement key management practices, including secure storage and rotation.
# - Use secure channels for transmitting the key and encrypted data.
# - After use, ensure sensitive data is securely deleted from memory (consider using libraries like `pycryptodome`).
# - Consider using authenticated encryption modes like GCM for additional integrity and authenticity.
# - Include versioning information with the encrypted data if necessary.
# - Protect against side-channel attacks where applicable.
# - Avoid logging sensitive information.

