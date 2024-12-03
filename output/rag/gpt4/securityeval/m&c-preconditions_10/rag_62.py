import os
import secrets
from django.core.management.utils import get_random_secret_key

def generate_crypto_key_django():
    """
    Generate a random 128-bit key using Django's get_random_secret_key() method.
    This is suitable for Django applications.
    """
    # Django's get_random_secret_key() generates a 50-character string
    # which is 400 bits if each character is 8 bits.
    # For a 128-bit key, we'll truncate the result.
    key = get_random_secret_key()
    return key[:16]  # Truncate to 128 bits (16 characters)

def generate_crypto_key_flask():
    """
    Generate a random 128-bit key using Python's secrets library.
    This is suitable for Flask applications.
    """
    # secrets.token_bytes generates a random byte string.
    # For a 128-bit key, we need 16 bytes.
    key = secrets.token_bytes(16)
    return key

# Example usage for a Django application
crypto_key_django = generate_crypto_key_django()
print(f"Django crypto key: {crypto_key_django}")

# Example usage for a Flask application
crypto_key_flask = generate_crypto_key_flask()
print(f"Flask crypto key: {crypto_key_flask.hex()}")  # Convert bytes to hex string for display

# Ensure Flask app is run with debugging disabled
# This should be set in the Flask app configuration
# app.config['DEBUG'] = False

