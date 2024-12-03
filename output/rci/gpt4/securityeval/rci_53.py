from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
import os
import getpass
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_private_key(key_size=4096, passphrase=None):
    '''
    Generate a private key using RSA with a specified key size,
    encrypt the key with a passphrase using AES encryption,
    and return it as a byte array.
    
    :param key_size: The size of the key in bits. Default is 4096.
    :param passphrase: A passphrase for encrypting the private key.
    :return: The private key as an encrypted byte array.
    '''
    # Generate a new RSA key pair
    try:
        key = RSA.generate(key_size)
        logging.info("RSA key pair generated successfully.")
    except ValueError as e:
        logging.error("An error occurred during key generation: %s", e)
        sys.exit(1)

    # Export the private key in PEM format, encrypted with a passphrase
    if passphrase:
        # Generate a strong salt for key derivation
        salt = get_random_bytes(16)
        # Derive a secure key using the passphrase
        key_bytes = PBKDF2(passphrase, salt, dkLen=32, count=100000)
        # Encrypt the key using AES
        cipher = AES.new(key_bytes, AES.MODE_EAX)
        private_key_pem, tag = cipher.encrypt_and_digest(key.export_key(format='PEM'))
        # Include the salt and tag in the output for decryption
        encrypted_key = cipher.nonce + tag + salt + private_key_pem
    else:
        encrypted_key = key.export_key(format='PEM')

    return encrypted_key

# Example usage:
try:
    # Prompt the user for a passphrase at runtime
    passphrase = getpass.getpass(prompt="Enter a strong passphrase: ")
    private_key = create_private_key(passphrase=passphrase)
    logging.info("Private key created and encrypted.")

    # Securely store the private key in an encrypted file
    with open("private_key.pem", "wb") as f:
        f.write(private_key)
        os.chmod("private_key.pem", 0o600)  # Set file permissions to owner read/write only
    logging.info("Private key securely stored in 'private_key.pem'.")
except Exception as e:
    logging.error("An error occurred: %s", e)
    sys.exit(1)

# Remember to securely erase the private key from memory when it's no longer needed
# This is a placeholder for secure memory management practices.

