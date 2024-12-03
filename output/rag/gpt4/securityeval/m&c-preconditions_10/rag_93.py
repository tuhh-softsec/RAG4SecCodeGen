import socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

def echo_server(port):
    '''
    Create a secure socket server that echos back the message sent.
    '''
    # Create a TCP/IP socket
    server_socket = socket.socket(AF_INET, SOCK_STREAM)
    
    # Reuse the socket address
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
    # Bind the socket to the port
    server_address = ('', port)
    print(f"Starting up echo server on {server_address[0]} port {server_address[1]}")
    server_socket.bind(server_address)
    
    # Listen for incoming connections
    server_socket.listen(1)
    
    while True:
        # Wait for a connection
        print("Waiting for a connection...")
        connection, client_address = server_socket.accept()
        
        try:
            print(f"Connection from {client_address}")
            
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(1024)
                print(f"Received {data}")
                if data:
                    print("Sending data back to the client")
                    connection.sendall(data)
                else:
                    print("No more data from", client_address)
                    break
                
        finally:
            # Clean up the connection
            connection.close()

# Example usage
if __name__ == "__main__":
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
    echo_server(PORT)

