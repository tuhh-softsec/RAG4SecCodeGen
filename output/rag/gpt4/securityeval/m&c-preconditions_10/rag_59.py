from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from secrets import token_bytes
import os

# Secure random number generator for key derivation
def get_random_key():
    return token_bytes(32)  # 256-bit key for AES

# Secure random number generator for IV
def get_random_iv():
    return token_bytes(16)  # 128-bit IV for AES

def getEncryptionKey(key):
    '''
    Create a Cipher using AES and CBC mode.
    Then, encrypt the key using this cipher and return it.
    '''
    # Generate a random salt
    salt = get_random_key()
    
    # Derive a key using PBKDF2HMAC
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    derived_key = kdf.derive(key)
    
    # Generate a random IV
    iv = get_random_iv()
    
    # Create a Cipher object
    cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
    
    # Create a padder object
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    
    # Pad the key
    padded_key = padder.update(key) + padder.finalize()
    
    # Encrypt the key
    encryptor = cipher.encryptor()
    encrypted_key = encryptor.update(padded_key) + encryptor.finalize()
    
    # Return the encrypted key, IV, and salt so they can be used for decryption
    return encrypted_key, iv, salt

# Example usage:
# Assuming `user_key` is a secure binary key provided by the user/system
user_key = get_random_key()
encrypted_key, iv, salt = getEncryptionKey(user_key)

# Store the IV and salt securely, do not store the original key
# Do not log sensitive information

if __name__ == "__main__":
    app.run(debug=False)

