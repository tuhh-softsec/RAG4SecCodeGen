import os
import getpass
from Crypto.PublicKey import ECC
from Crypto.IO import PEM
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, filename='keygen.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def generate_private_key(passphrase):
    '''
    Generate a private key using ECDSA with Curve25519,
    export the key in PEM format with encryption,
    then return it.
    
    :param passphrase: A passphrase for encrypting the private key.
    :return: The encrypted private key in PEM format.
    '''
    try:
        # Generate a new ECDSA key with Curve25519
        key = ECC.generate(curve='P-256')  # Consider using curve='Ed25519' for better security

        # Export the private key in PEM format, encrypted with the provided passphrase
        private_key_pem = key.export_key(
            format='PEM',
            passphrase=passphrase,
            protection="PBKDF2WithHMAC-SHA256AndAES256-CBC"  # Stronger key derivation and encryption
        )

        return private_key_pem
    except Exception as e:
        logging.error(f"An error occurred during key generation: {e}")
        raise

def get_secure_passphrase():
    '''
    Obtain a passphrase securely. Validate its strength and return it.
    '''
    passphrase = getpass.getpass(prompt="Enter a secure passphrase: ")
    # Implement passphrase strength validation here (e.g., minimum length, complexity)
    if len(passphrase) < 12 or not complex_passphrase(passphrase):
        raise ValueError("Passphrase does not meet the complexity requirements.")
    return passphrase

def complex_passphrase(passphrase):
    # Implement your passphrase complexity check here
    # For example, check for a mix of letters, numbers, and special characters
    return True  # Replace with actual complexity check

# Example usage:
try:
    passphrase = get_secure_passphrase()  # Securely obtain the passphrase
    private_key = generate_private_key(passphrase)
    print(private_key)
except Exception as e:
    logging.error(f"An error occurred: {e}")

# Security considerations:
# - Use a secure method to obtain the passphrase, such as prompting the user or using an environment variable.
# - Validate the strength of the passphrase to resist brute-force attacks.
# - Use stronger key derivation and encryption algorithms, such as PBKDF2 with HMAC-SHA256 and AES256.
# - Log errors appropriately without exposing sensitive information.
# - Verify the integrity of the `pycryptodome` library upon installation.
# - Ensure the private key is transmitted securely using protocols like SSH or TLS.
# - Store the private key in secure storage solutions designed to protect cryptographic keys.
# - Regularly review and update cryptographic methods and libraries to address deprecation and vulnerabilities.
# - Implement audit logging to track key generation and access.

