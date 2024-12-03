import socket
import ssl
import os
import threading
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up a thread pool executor for handling client connections
executor = ThreadPoolExecutor(max_workers=10)

def handle_client(secure_connection, client_address):
    try:
        logging.info(f'Connection from {client_address}')

        # Set a timeout for blocking operations
        secure_connection.settimeout(10.0)

        # Receive the data in small chunks and retransmit it
        while True:
            try:
                data = secure_connection.recv(1024)
                if data:
                    # Perform input validation or sanitization here if necessary
                    logging.info(f'Received: {data.decode()}')
                    secure_connection.sendall(data)
                else:
                    logging.info(f'No more data from {client_address}')
                    break
            except socket.timeout:
                logging.warning(f'Timeout from {client_address}')
                break
    except (ssl.SSLError, ssl.CertificateError, ssl.SSLEOFError) as e:
        logging.error(f'SSL error from {client_address}: {e}')
    except Exception as e:
        logging.error(f'Unexpected error from {client_address}: {e}')
    finally:
        # Clean up the connection
        try:
            secure_connection.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        secure_connection.close()

def echo_server(port, certfile, keyfile):
    # Ensure the certificate and key files exist and have appropriate permissions
    cert_path = Path(certfile)
    key_path = Path(keyfile)
    if not cert_path.is_file() or not key_path.is_file():
        raise FileNotFoundError("Certificate or key file not found.")
    os.chmod(certfile, 0o400)
    os.chmod(keyfile, 0o400)

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('', port)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(5)

    # Wrap the socket with SSL/TLS
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    # Require client certificate (optional, for client authentication)
    # context.verify_mode = ssl.CERT_REQUIRED
    # context.load_verify_locations('path/to/client_cert.pem')

    logging.info(f'Server is running on port {port}. Waiting for a connection...')

    while True:
        # Wait for a connection
        connection, client_address = sock.accept()

        # Wrap the client's connection with SSL/TLS
        secure_connection = context.wrap_socket(connection, server_side=True)

        # Submit the client connection to the thread pool executor
        executor.submit(handle_client, secure_connection, client_address)

# Example usage:
if __name__ == '__main__':
    # Load paths from environment variables or default to hardcoded paths
    CERTFILE = os.getenv('CERTFILE', 'path/to/certificate.pem')
    KEYFILE = os.getenv('KEYFILE', 'path/to/private_key.pem')
    PORT = int(os.getenv('PORT', 65432))

    try:
        echo_server(PORT, CERTFILE, KEYFILE)
    except KeyboardInterrupt:
        logging.info("Server is shutting down.")
        executor.shutdown(wait=True)

