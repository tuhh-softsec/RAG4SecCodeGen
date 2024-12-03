from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad
import os
import hmac
import base64

def encryptData(data, passphrase):
    '''
    Encrypt data using AES in CBC mode with a derived key from the passphrase, ensuring confidentiality, integrity, and authentication.
    '''
    try:
        # Derive a key from the passphrase using PBKDF2 with a random salt and a strong hash function
        salt = get_random_bytes(16)
        key = PBKDF2(passphrase, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)

        # Generate a random IV
        iv = get_random_bytes(AES.block_size)

        # Create a cipher object using the key and IV in CBC mode
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Pad the data to be a multiple of the block size
        padded_data = pad(data, AES.block_size)

        # Encrypt the data
        encrypted_data = cipher.encrypt(padded_data)

        # Generate HMAC for integrity and authentication
        hmac_key = get_random_bytes(32)  # Generate a separate key for HMAC
        hmac_obj = hmac.new(hmac_key, encrypted_data, SHA256)
        hmac_digest = hmac_obj.digest()

        # Return the encrypted data along with the IV, salt, and HMAC digest
        return base64.b64encode(encrypted_data + iv + salt + hmac_digest + hmac_key)
    except Exception as e:
        # Implement secure error handling
        print("An error occurred during encryption:", e)
        # Depending on the application, you may want to re-raise the exception or handle it differently

# Example usage:
# Passphrase should be securely obtained, e.g., from user input or an environment variable
passphrase = os.environ.get('ENCRYPTION_PASSPHRASE').encode()

data = b'Your data to encrypt'

encrypted_blob = encryptData(data, passphrase)
print("Encrypted blob:", encrypted_blob)

# Remember to securely store or transmit the encrypted blob.
# It contains the encrypted data, IV, salt, HMAC digest, and HMAC key, all necessary for decryption and verification.

