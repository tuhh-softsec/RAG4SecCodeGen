import os
import stat
import logging
from OpenSSL import SSL

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration variables (should be set via environment variables or a config file)
CERT_FILE_PATH = os.getenv('CERT_FILE_PATH')
KEY_FILE_PATH = os.getenv('KEY_FILE_PATH')

if not CERT_FILE_PATH or not KEY_FILE_PATH:
    raise ValueError("Environment variables for CERT_FILE_PATH and KEY_FILE_PATH must be set.")

def load_certificate_and_key(context, cert_file, key_file):
    # Check file permissions to ensure that the private key file is protected
    key_permissions = os.stat(key_file).st_mode
    if key_permissions & (stat.S_IRWXG | stat.S_IRWXO):
        raise PermissionError("Private key file permissions are too open.")

    # Load the server's certificate and private key
    context.use_certificate_file(cert_file)
    context.use_privatekey_file(key_file)

    # Check that the private key and certificate match
    context.check_privatekey()

def create_ssl_context():
    '''
    Create an OpenSSL context with enhanced security settings.
    '''

    # Create a new context using the strongest available SSL/TLS protocol
    context = SSL.Context(SSL.TLSv1_3_METHOD)

    # Set the context to verify the server certificate
    def verify_callback(connection, x509, errnum, errdepth, ok):
        # Custom verification logic goes here
        # For example, hostname verification could be implemented here
        return ok

    context.set_verify(SSL.VERIFY_PEER, callback=verify_callback)

    # Load the server's certificate and private key
    load_certificate_and_key(context, CERT_FILE_PATH, KEY_FILE_PATH)

    # Set options to provide a high level of security
    context.set_options(SSL.OP_NO_SSLv2 | SSL.OP_NO_SSLv3 | SSL.OP_NO_TLSv1 | SSL.OP_NO_TLSv1_1)

    # Specify strong cipher suites and disable weak ones
    context.set_cipher_list('HIGH:!aNULL:!kRSA:!PSK:!SRP:!MD5:!RC4')

    # Configure session resumption and tickets
    context.set_session_cache_mode(SSL.SESS_CACHE_OFF)

    # Implement certificate revocation checks (CRLs or OCSP)
    # This is a placeholder for actual implementation
    # context.set_ocsp_stapling(True)

    return context

# Example usage
try:
    context = create_ssl_context()
except FileNotFoundError as e:
    logger.error(f"Certificate or key file not found: {e}")
except PermissionError as e:
    logger.error(f"File permission error: {e}")
except SSL.Error as e:
    logger.error(f"OpenSSL error: {e}")
except Exception as e:
    logger.error(f"An unexpected error occurred: {e}")

# Note: Replace the placeholder environment variables with actual values before running the code.

