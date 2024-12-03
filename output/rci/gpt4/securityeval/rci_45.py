import ssl
import os
import logging
import pwd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def getSSLContext(certfile_path, keyfile_path, cafile_path=None):
    '''
    Create an SSL context with secure default settings and return it.
    
    :param certfile_path: Path to the certificate file
    :param keyfile_path: Path to the private key file
    :param cafile_path: Path to the CA bundle file (optional)
    :return: Configured SSL context
    '''
    # Check if the files exist and have the correct permissions before use
    for path in [certfile_path, keyfile_path, cafile_path]:
        if path and not os.path.isfile(path):
            raise FileNotFoundError(f"File not found: {path}")
        if path and os.stat(path).st_mode & 0o777 != 0o600:
            raise PermissionError(f"File permissions for {path} are not set to 0o600.")

    # Check if the current user is the owner of the files
    current_user = pwd.getpwuid(os.getuid()).pw_name
    for path in [certfile_path, keyfile_path]:
        if path and pwd.getpwuid(os.stat(path).st_uid).pw_name != current_user:
            raise PermissionError(f"File {path} is not owned by the current user: {current_user}")

    # Create a default context with secure settings
    context = ssl.create_default_context()

    # Load the server's certificate and private key
    context.load_cert_chain(certfile=certfile_path, keyfile=keyfile_path)

    # If a custom CA bundle is provided, use it to verify peer certificates
    if cafile_path and os.path.isfile(cafile_path):
        context.load_verify_locations(cafile=cafile_path)

    # Require certificate verification
    context.verify_mode = ssl.CERT_REQUIRED

    # Enable hostname checking
    context.check_hostname = True

    # Optionally, you can customize the context further, for example:
    # - Set allowed cipher suites with context.set_ciphers()
    # - Enable or disable session resumption
    # - Enforce perfect forward secrecy by selecting appropriate cipher suites

    # Ensure that you are using the latest version of Python and the ssl module
    # to have access to the most secure protocol versions and features.

    # Use configuration files or environment variables to manage file paths
    # and other sensitive information in a production environment.

    # Consider implementing certificate revocation checks if required for your application's security.

    return context

# Example usage:
try:
    ssl_context = getSSLContext(
        certfile_path=os.getenv('CERTFILE_PATH', 'path/to/cert.pem'),
        keyfile_path=os.getenv('KEYFILE_PATH', 'path/to/key.pem'),
        cafile_path=os.getenv('CAFILE_PATH', 'path/to/cabundle.pem')  # Optional: specify if using a custom CA bundle
    )
except FileNotFoundError as e:
    logger.error(f"File not found: {e}")
except PermissionError as e:
    logger.error(f"Permission error: {e}")
except ssl.SSLError as e:
    logger.error(f"SSL error: {e}")
except Exception as e:
    logger.error(f"An unexpected error occurred: {e}")

