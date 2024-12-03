from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hmac, hashes
from cryptography.exceptions import InvalidSignature
from os import urandom

def generate_random_key_and_iv(key_size=32):
    # Validate key size
    if key_size not in (16, 24, 32):
        raise ValueError("Invalid key size. Choose 16, 24, or 32 bytes.")
    key = urandom(key_size)
    iv = urandom(16)  # AES block size is 16 bytes
    return key, iv

def encrypt_data(data, key=None):
    '''
    Encrypt the data using AES in CBC mode with HMAC for data integrity and return the encrypted data, IV, and HMAC.
    If a key is not provided, generate a new one.
    '''
    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes.")
    
    # Generate a random key and IV if a key is not provided
    if key is None:
        key, iv = generate_random_key_and_iv()
    else:
        if len(key) not in (16, 24, 32):
            raise ValueError("Key must be 16, 24, or 32 bytes.")
        iv = urandom(16)  # Always generate a new IV for each encryption

    # Create a Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    # Create a padder to pad the data to the block size required by the cipher
    padder = padding.PKCS7(algorithms.AES.block_size).padder()

    # Create HMAC object for authentication
    hmac_key = urandom(32)  # Generate a separate key for HMAC
    hmac_obj = hmac.HMAC(hmac_key, hashes.SHA256(), backend=default_backend())

    try:
        # Pad the data
        padded_data = padder.update(data) + padder.finalize()

        # Create an encryptor object
        encryptor = cipher.encryptor()

        # Encrypt the padded data
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Calculate HMAC
        hmac_obj.update(encrypted_data)
        hmac_digest = hmac_obj.finalize()

    except Exception as e:
        # Handle encryption errors without revealing sensitive information
        raise EncryptionError("Encryption failed.") from None

    # Return the encrypted data, IV, and HMAC digest
    return encrypted_data, iv, hmac_digest, hmac_key

# Define a custom exception for encryption errors
class EncryptionError(Exception):
    pass

# Example usage:
# Assuming `data_to_encrypt` is the data you want to encrypt (bytes type)
data_to_encrypt = b"my secret data"
try:
    encrypted_data, iv, hmac_digest, hmac_key = encrypt_data(data_to_encrypt)
    print("Encrypted data:", encrypted_data)
    print("IV:", iv)
    print("HMAC Digest:", hmac_digest)
except EncryptionError as e:
    print("An error occurred: ", e)

# Remember to securely manage the key, IV, and HMAC key:
# - Store the keys in a secure key management system or hardware security module.
# - Transmit the IV and HMAC digest securely alongside the encrypted data.
# - Use authenticated encryption to ensure data integrity and authenticity.
# - Securely delete sensitive data from memory when no longer needed, using libraries that provide secure deletion capabilities.

