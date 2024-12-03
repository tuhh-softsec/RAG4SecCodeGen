from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import os

# Securely generate a random initialization vector (IV)
def generate_iv(block_size):
    return get_random_bytes(block_size)

def get_encryption_key(data, key):
    '''
    Create a static vector, cipher using AES and CBC mode
    encrypt the data using the cipher by padding up to the block_size, and return it
    '''
    # Ensure the key length is valid for AES (16, 24, 32 bytes)
    if len(key) not in [16, 24, 32]:
        raise ValueError("Invalid key size. Key must be 16, 24, or 32 bytes long.")

    # Generate a secure random IV
    iv = generate_iv(AES.block_size)

    # Create the cipher object using AES in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Pad the data to be a multiple of the block size
    padded_data = pad(data, AES.block_size)

    # Encrypt the data
    encrypted_data = cipher.encrypt(padded_data)

    # Return the IV and encrypted data together
    return iv + encrypted_data

# Example usage:
# Securely generate a random key (for demonstration purposes)
# In a real-world scenario, the key should be securely stored and managed.
key = get_random_bytes(32)  # AES-256
data = b"Secret data that needs to be encrypted"

encrypted = get_encryption_key(data, key)
print("Encrypted data:", encrypted)

