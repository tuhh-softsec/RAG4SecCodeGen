from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, serialization, hashes, kdf
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hmac import HMAC
from os import urandom
import secrets
import base64

# Constants for key derivation
SALT_LENGTH = 16
ITERATIONS = 100000
KEY_LENGTH = 32  # 256 bits for AES-256

def get_random_iv():
    # Use a secure random generator to create an initialization vector
    return urandom(algorithms.AES.block_size // 8)

def derive_key(password, salt, iterations=ITERATIONS, key_length=KEY_LENGTH):
    """
    Derive a cryptographic key from a password using PBKDF2.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=key_length,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_data(data, key, iv):
    """
    Encrypt data using AES GCM mode with the provided key and IV.
    Includes padding and returns base64 encoded ciphertext and tag for authentication.
    """
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return base64.b64encode(ciphertext), base64.b64encode(encryptor.tag)

def get_encryption_key(password):
    """
    Generate a secure encryption key based on a password.
    """
    # Generate a random salt
    salt = secrets.token_bytes(SALT_LENGTH)
    
    # Derive a key from the password
    encryption_key = derive_key(password, salt)
    
    # Generate a random IV
    iv = get_random_iv()

    # Encrypt the data with the derived key
    # Note: In a real-world scenario, you would encrypt actual data, not the key itself.
    # The following line is for demonstration purposes only.
    encrypted_data, tag = encrypt_data(b"Sensitive data to encrypt", encryption_key, iv)

    # Return the encrypted data, tag, IV, and salt, all base64 encoded for safe storage/transmission
    return {
        'encrypted_data': encrypted_data.decode('utf-8'),
        'tag': tag.decode('utf-8'),
        'iv': base64.b64encode(iv).decode('utf-8'),
        'salt': base64.b64encode(salt).decode('utf-8')
    }

# Example usage:
# result = get_encryption_key('sensitive_password')
# print(f'Encrypted Data: {result["encrypted_data"]}')
# print(f'Tag: {result["tag"]}')
# print(f'IV: {result["iv"]}')
# print(f'Salt: {result["salt"]}')

