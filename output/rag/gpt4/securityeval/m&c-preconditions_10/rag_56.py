import socket
import ssl

# Define a maximum number of connections to prevent resource exhaustion
MAX_CONNECTIONS = 5
connection_count = 0

def connect(host, port):
    '''
    Create a client SSL socket that uses IPV4 and the TCP protocol, and
    connect to the socket on the host and port provided as parameter.
    Then, return the socket.
    '''
    global connection_count

    # Check if we have reached the maximum number of connections
    if connection_count >= MAX_CONNECTIONS:
        raise ConnectionError("Maximum number of connections reached")

    # Create a socket using IPV4 and TCP protocol
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wrap the socket with SSL for secure communication
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Enforce TLSv1.2 or higher
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    context.load_default_certs()  # Load default CA certificates

    # Connect to the server with SSL
    secure_sock = context.wrap_socket(sock, server_hostname=host)

    try:
        secure_sock.connect((host, port))
        connection_count += 1
        return secure_sock
    except Exception as e:
        secure_sock.close()
        raise e

# Example usage
if __name__ == "__main__":
    host = 'example.com'
    port = 443
    try:
        ssl_socket = connect(host, port)
        print(f"Connected to {host} on port {port}")
        # Perform secure communication with the server here
    finally:
        ssl_socket.close()
        connection_count -= 1

