import os
import time
import base64
import logging
from cryptography.hazmat.primitives import hashes, padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hmac

# Configure secure logging (without sensitive information)
logging.basicConfig(filename='encryption.log', level=logging.ERROR)

# Secure key derivation function
def derive_key(password, salt, iterations=200000):  # Increased iterations
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(password)

# Securely send encrypted message
def send_encrypted(secret_key, channel, message):
    try:
        # Generate a random salt for encryption and HMAC
        encryption_salt = os.urandom(16)
        hmac_salt = os.urandom(16)
        iv = os.urandom(12)  # GCM mode uses a 12-byte IV

        # Derive keys using the provided secret_key and salts
        encryption_key = derive_key(secret_key, encryption_salt)
        hmac_key = derive_key(secret_key, hmac_salt)

        # Create a cipher object using the derived key and IV
        cipher = Cipher(algorithms.AES(encryption_key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Pad the message using PKCS7 padding
        padder = sym_padding.PKCS7(algorithms.AES.block_size).padder()
        padded_message = padder.update(message.encode()) + padder.finalize()

        # Encrypt the message
        encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
        tag = encryptor.tag

        # Create a timestamp to ensure message freshness
        timestamp = int(time.time())

        # Create HMAC to ensure message integrity
        h = hmac.HMAC(hmac_key, hashes.SHA256(), backend=default_backend())
        h.update(encrypted_message)
        h.update(iv)
        h.update(tag)
        h.update(str(timestamp).encode())
        message_hmac = h.finalize()

        # Encode the components to make them safe to send over the channel
        encoded_message = base64.b64encode(encrypted_message).decode()
        encoded_iv = base64.b64encode(iv).decode()
        encoded_tag = base64.b64encode(tag).decode()
        encoded_encryption_salt = base64.b64encode(encryption_salt).decode()
        encoded_hmac_salt = base64.b64encode(hmac_salt).decode()
        encoded_hmac = base64.b64encode(message_hmac).decode()

        # Send the encrypted message over the channel with the IV, salts, HMAC, tag, and timestamp
        channel.send({
            'message': encoded_message,
            'iv': encoded_iv,
            'tag': encoded_tag,
            'encryption_salt': encoded_encryption_salt,
            'hmac_salt': encoded_hmac_salt,
            'hmac': encoded_hmac,
            'timestamp': timestamp
        })
    except Exception as e:
        # Handle exceptions securely
        logging.error("An error occurred: %s", str(e))  # Log the error securely
        print("An error occurred during encryption or transmission.")

# Example usage:
# Assuming `channel` is an authenticated and secure communication object with a `send` method
# secret_key should be a strong, randomly generated key, handled as bytes
# message is the plaintext message to be sent
send_encrypted(os.urandom(32), channel, 'Your secret message')

