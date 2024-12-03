import hashlib
import hmac
import os
from getpass import getpass

def generate_salt():
    # Generates a secure random salt
    return os.urandom(16)

def hash_certificate_with_salt(certificate, salt):
    # Hashes the certificate with the given salt using SHA-256
    return hashlib.pbkdf2_hmac('sha256', certificate.encode(), salt, 100000)

def certificate_matches(certificate, known_hash, salt):
    '''
    Return true if the certificate matches the known_hash.
    '''
    # Hash the certificate with the provided salt
    certificate_hash = hash_certificate_with_salt(certificate, salt)
    
    # Securely compare the computed hash with the known hash
    return hmac.compare_digest(certificate_hash, known_hash)

# Example usage:
# Assuming we have a known hash and salt stored securely
# For demonstration purposes, we will generate them here
known_certificate = "example_certificate_content"
salt = generate_salt()
known_hash = hash_certificate_with_salt(known_certificate, salt)

# Now we can check if another certificate matches the known hash
certificate_to_check = "example_certificate_content"
if certificate_matches(certificate_to_check, known_hash, salt):
    print("Certificate matches the known hash.")
else:
    print("Certificate does not match the known hash.")

