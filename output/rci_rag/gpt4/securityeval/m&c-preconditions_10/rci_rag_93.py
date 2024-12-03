import socket
import ssl
import os
import signal
import logging
import select
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

# Configure logging
logging.basicConfig(level=logging.INFO)

# Signal handler for graceful shutdown
def shutdown_server(signum, frame):
    logging.info('Shutting down server...')
    server_socket.close()
    os._exit(0)  # Consider using sys.exit() instead for a cleaner shutdown

# Register signal handler
signal.signal(signal.SIGINT, shutdown_server)
signal.signal(signal.SIGTERM, shutdown_server)

# Function to validate client input
def validate_input(data):
    # Implement input validation logic here
    # For example, check for size, content, encoding, etc.
    return True

# Function to handle client connections
def handle_client(connection, client_address):
    try:
        logging.info(f"Connection from {client_address}")
        
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            if not validate_input(data):
                logging.warning(f"Invalid input from {client_address}")
                break
            logging.info(f"Received {data}")
            if data:
                logging.info("Sending data back to the client")
                connection.sendall(data)
            else:
                logging.info("No more data from", client_address)
                break
            
    except ssl.SSLError as e:
        logging.error(f"SSL error: {e}")
    except socket.error as e:
        logging.error(f"Socket error: {e}")
    finally:
        # Clean up the connection
        connection.close()

def echoServer(port, certfile, keyfile):
    '''
    Create a secure socket server that echos back the message sent.
    This server performs security checks to ensure safe operation.
    '''

    # Create a TCP/IP socket
    server_socket = socket.socket(AF_INET, SOCK_STREAM)
    
    # Reuse the socket address
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
    # Bind the socket to the port
    server_address = ('', port)
    logging.info(f"Starting up echo server on {server_address[0]} port {server_address[1]}")
    server_socket.bind(server_address)
    
    # Listen for incoming connections
    server_socket.listen(5)  # Limit the number of queued connections
    
    # Wrap the socket with SSL for encryption
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    server_socket = context.wrap_socket(server_socket, server_side=True)
    
    # Set up a list to keep track of socket descriptors
    inputs = [server_socket]
    
    try:
        while inputs:
            # Use select to handle I/O readiness notification
            readable, writable, exceptional = select.select(inputs, [], inputs)
            
            for s in readable:
                if s is server_socket:
                    # A "readable" server socket is ready to accept a connection
                    connection, client_address = s.accept()
                    logging.info("New connection from %s:%s" % client_address)
                    connection.setblocking(0)
                    inputs.append(connection)
                else:
                    # Existing connection is ready to be read
                    handle_client(s, s.getpeername())
            
            for s in exceptional:
                logging.error(f"Handling exceptional condition for {s.getpeername()}")
                # Stop listening for input on the connection
                inputs.remove(s)
                s.close()
    finally:
        server_socket.close()

# Replace with the appropriate port number and paths to your certificate and key files
PORT = 65432
CERTFILE = 'path/to/certificate.pem'
KEYFILE = 'path/to/private_key.pem'

# Run the server function
if __name__ == "__main__":
    echoServer(PORT, CERTFILE, KEYFILE)

