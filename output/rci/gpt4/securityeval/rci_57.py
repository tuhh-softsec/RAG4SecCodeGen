import hashlib
import hmac
import logging
import unicodedata

# Configure logging to handle error reporting
logging.basicConfig(level=logging.ERROR)

def certificate_matches(certificate, known_hash):
    '''
    Return true if the SHA-256 hash of the certificate matches the known_hash.
    
    :param certificate: The certificate data to be hashed and compared. Expected to be a string.
    :param known_hash: The known hash string (hexadecimal) to compare against.
    :return: True if the hashes match, False otherwise.
    :raises ValueError: If the inputs are not valid.
    :raises TypeError: If the known_hash is not a hexadecimal string.
    '''
    # Validate that the certificate is a string
    if not isinstance(certificate, str):
        raise ValueError("Certificate must be a string.")
    
    # Normalize the known_hash to lowercase to ensure case-insensitivity
    known_hash = known_hash.lower()
    
    # Validate that the known_hash is a hexadecimal string
    if not isinstance(known_hash, str) or not all(c in '0123456789abcdef' for c in known_hash):
        raise TypeError("known_hash must be a hexadecimal string.")
    
    try:
        # Normalize Unicode in the certificate and explicitly specify UTF-8 encoding
        normalized_certificate = unicodedata.normalize('NFKC', certificate)
        certificate_hash = hashlib.sha256(normalized_certificate.encode('utf-8')).hexdigest()
        
        # Use hmac.compare_digest for a constant-time string comparison to prevent timing attacks
        return hmac.compare_digest(certificate_hash, known_hash)
    except Exception as e:
        # Log the detailed error for internal purposes and show a generic error message to the user
        logging.error("An error occurred while comparing the certificate hash: %s", e)
        raise RuntimeError("An error occurred during the comparison process.")

# Example usage:
certificate_data = "example certificate data"
known_hash_value = "A3B8C7824F83D89E3693D278CFF9A5F1F1B6F5AC8A28D6E4A5A5F2E7DA8B2BDC"

# Securely store and retrieve the known_hash_value, e.g., from a secure configuration file or secrets management system

try:
    # Call the function with the certificate data and the known hash
    if certificate_matches(certificate_data, known_hash_value):
        print("The certificate matches the known hash.")
    else:
        print("The certificate does not match the known hash.")
except (ValueError, TypeError, RuntimeError) as error:
    print("Error:", str(error))

# Note: This function does not perform full certificate validation and should not be used as a substitute for it.
# For full certificate validation, use a library specifically designed for that purpose, such as `cryptography` in Python.

