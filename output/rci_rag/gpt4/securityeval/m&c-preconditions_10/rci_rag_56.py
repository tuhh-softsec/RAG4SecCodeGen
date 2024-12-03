import socket
import ssl
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect(host, port, ca_cert=None, cipher_suites=None):
    '''
    Create a client SSL socket that uses IPV4 and the TCP protocol, and
    connect to the socket on the host and port provided as parameter.
    Then, return the socket.
    '''
    # Create a secure SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)  # Enforce latest TLS version
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED

    # Load custom CA certificate if provided for certificate pinning
    if ca_cert:
        context.load_verify_locations(ca_cert)

    # Set cipher suites if provided
    if cipher_suites:
        context.set_ciphers(cipher_suites)

    # Create a socket using the IPv4 address family and TCP protocol
    try:
        with socket.create_connection((host, port)) as sock:
            # Wrap the socket with SSL for encryption
            with context.wrap_socket(sock, server_hostname=host) as ssl_sock:
                # Now you can use ssl_sock to send and receive data securely
                # Perform any necessary data transfer here
                pass
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

# Example usage
if __name__ == "__main__":
    host = os.getenv('HOST', 'example.com')  # Get host from environment variable or default
    port = int(os.getenv('PORT', '443'))     # Get port from environment variable or default
    ca_cert = os.getenv('CA_CERT_PATH')      # Path to a custom CA certificate for pinning
    cipher_suites = os.getenv('CIPHER_SUITES')  # String of cipher suites to use

    try:
        connect(host, port, ca_cert, cipher_suites)
    except (socket.error, ssl.SSLError, ssl.CertificateError) as e:
        logging.error(f"Connection error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        # Any necessary cleanup can be performed here
        pass

# Note: It's important to handle exceptions to gracefully handle connection errors and certificate verification problems.
# Additionally, ensure that the socket is properly closed after use, which is handled by the context manager in this example.

