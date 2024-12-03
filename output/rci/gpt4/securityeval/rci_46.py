import os
import logging
from OpenSSL import SSL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_certificate_and_key(context, cert_path, key_path):
    '''
    Load the server's certificate and private key with secure file permissions.
    '''
    # Check file permissions to ensure they are set securely
    for path in (cert_path, key_path):
        if os.stat(path).st_mode & 0o777 != 0o600:
            logger.error(f"File permissions for {path} are not secure!")
            raise PermissionError(f"Insecure file permissions for {path}")

    # Load the certificate and private key
    try:
        context.use_certificate_file(cert_path)
        context.use_privatekey_file(key_path)
        context.check_privatekey()  # Verify that the private key matches the certificate
    except Exception as e:
        logger.exception("An error occurred while loading the certificate or private key.")
        raise

def configure_context(context):
    '''
    Configure the OpenSSL context with secure settings.
    '''
    # Set options to provide a higher level of security
    context.set_options(SSL.OP_NO_SSLv2 | SSL.OP_NO_SSLv3 | SSL.OP_NO_TLSv1 | SSL.OP_NO_TLSv1_1 | SSL.OP_CIPHER_SERVER_PREFERENCE)

    # Set a strong cipher suite. This should be regularly reviewed and updated.
    context.set_cipher_list('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')

    # Implement hostname verification if this context is used for client connections
    # This is critical for preventing Man-in-the-Middle (MitM) attacks.
    # Example: context.set_tlsext_host_name(server_hostname)

    # Ensure that the OpenSSL library is properly configured to use a secure random number generator.
    # This is typically handled by the library itself and the underlying operating system.

    # Consider enabling or disabling session resumption and ticketing based on your specific use case.
    # context.set_session_cache_mode(SSL.SESS_CACHE_OFF)

    # Require client certificate verification if needed
    # context.set_verify(SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT, callback_function)

    # Implement OCSP stapling if applicable
    # context.set_tlsext_status_type(SSL.TLSEXT_STATUSTYPE_ocsp)

    # Implement rate limiting or connection throttling to mitigate DoS attacks
    # This is typically handled at a higher level, such as a web server or load balancer.

    # Implement HSTS if this context is used for a web server
    # This is typically handled at the application level, not within the SSL context.

def getContext(cert_path='server.crt', key_path='server.key'):
    '''
    Create an OpenSSL context with secure default settings and return it.
    '''
    # Create a new context using the TLS method, which chooses the highest protocol version that both the client and server support.
    context = SSL.Context(SSL.TLS_METHOD)

    # Load the server's certificate and private key
    load_certificate_and_key(context, cert_path, key_path)

    # Configure the context with secure settings
    configure_context(context)

    # Implement logging and monitoring as appropriate for your application.
    # Example: logger.info("SSL context successfully created.")

    return context

# Example usage
if __name__ == "__main__":
    # Paths to the certificate and key files should be configurable
    CERT_FILE_PATH = os.getenv('CERT_FILE_PATH', 'server.crt')
    KEY_FILE_PATH = os.getenv('KEY_FILE_PATH', 'server.key')

    try:
        ssl_context = getContext(CERT_FILE_PATH, KEY_FILE_PATH)
        logger.info("SSL context successfully created.")
        # Now you can use ssl_context to create secure SSL/TLS connections
    except Exception as e:
        logger.error("Failed to create SSL context.", exc_info=True)

