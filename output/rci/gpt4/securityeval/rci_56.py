import socket
import ssl
import logging

# Configure logging for monitoring and debugging
logging.basicConfig(level=logging.INFO)

def connect(host, port, client_cert=None, client_key=None, ca_cert=None):
    '''
    Create a client SSL socket that uses IPV4 and the TCP protocol, and
    connect to the socket on the host and port provided as parameter.
    Optionally, use client certificates for mutual TLS authentication.
    Then, return the socket.
    '''
    sock = None
    try:
        # Create a socket using IPv4 (AF_INET) and TCP protocol (SOCK_STREAM)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Create an SSL context with secure default settings
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

        # Explicitly set the SSL/TLS protocol version to TLS 1.2 or higher
        ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2

        # Load custom CA bundle if provided, otherwise use default system CA certificates
        if ca_cert:
            ssl_context.load_verify_locations(ca_cert)
        else:
            ssl_context.load_default_certs()

        # Specify the cipher suites to be used
        ssl_context.set_ciphers('HIGH:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!3DES:!MD5:!PSK')

        # Enable hostname checking
        ssl_context.check_hostname = True

        # Load client certificate and key if provided for mutual TLS authentication
        if client_cert and client_key:
            ssl_context.load_cert_chain(certfile=client_cert, keyfile=client_key)

        # Wrap the socket to create an SSL socket
        ssl_sock = ssl_context.wrap_socket(sock, server_hostname=host)

        # Connect to the server
        ssl_sock.connect((host, port))

        # Log successful connection
        logging.info(f"Successfully connected to {host}:{port}")

        # Return the SSL socket
        return ssl_sock

    except ssl.SSLError as e:
        logging.error(f"SSL error occurred: {e}")
        raise e
    except socket.error as e:
        logging.error(f"Socket error occurred: {e}")
        raise e
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise e
    finally:
        # Ensure the socket is closed in case of any exception
        if sock is not None:
            sock.close()

# Example usage:
try:
    # Replace 'example.com' with the actual host and 443 with the actual port
    with connect('example.com', 443) as secure_socket:
        # Use secure_socket to send and receive data securely
        pass  # Replace with actual data transfer code

    # The socket is automatically closed when exiting the 'with' block
except Exception as e:
    logging.error(f"Failed to create a secure socket: {e}")

# Note: Additional hardening of the SSL context, handling of TOCTOU issues,
# and implementation of session resumption should be considered based on
# specific security requirements and operational context.

