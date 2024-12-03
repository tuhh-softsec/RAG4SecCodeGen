from Crypto.PublicKey import RSA
import os
from getpass import getpass

def create_private_key(key_length=2048, passphrase=None):
    """
    Generate a private key using RSA and export the key.

    Parameters:
    - key_length: The length of the key in bits. Recommended minimum is 2048 bits.
    - passphrase: Optional passphrase for encrypting the key. If not provided, the user will be prompted.

    Returns:
    The private key in PEM format, encrypted if a passphrase is provided.

    Raises:
    - ValueError: If the key_length is not an integer or below the recommended minimum.
    - OSError: If there is an error during key generation due to the operating system.
    - Exception: For other unexpected issues.

    Note:
    - Ensure that the underlying operating system's implementation of os.urandom is secure.
    - Keep the PyCryptodome library up-to-date to address any security vulnerabilities.
    - Handle the private key securely after generation and avoid exposing it.
    - Consider using secure memory handling techniques to avoid exposing sensitive data in memory.
    """
    if not isinstance(key_length, int) or key_length < 2048:
        raise ValueError("Key length must be an integer and at least 2048 bits.")

    if passphrase is None:
        passphrase = getpass("Enter passphrase for private key encryption: ")

    try:
        # Generate a private RSA key
        key = RSA.generate(key_length, os.urandom)

        # Export the private key in PEM format, encrypted if a passphrase is provided
        private_key = key.export_key(passphrase=passphrase, pkcs=8, protection="scryptAndAES128-CBC")

        # Securely delete the key variable from memory
        del key

        return private_key
    except ValueError as e:
        raise ValueError(f"Invalid parameter: {e}")
    except OSError as e:
        raise OSError(f"An error occurred during key generation: {e}")
    except Exception as e:
        # Log the exception internally and raise a generic exception message
        # log_exception(e)  # Assume log_exception is a function that logs the error
        raise Exception("An unexpected error occurred during key generation.")

# Example usage
if __name__ == "__main__":
    try:
        private_key = create_private_key()
        # In a real-world scenario, you would securely store the private key
        # For demonstration purposes, we will not print or expose the private key here.
    except Exception as e:
        print(f"An error occurred: {e}")

