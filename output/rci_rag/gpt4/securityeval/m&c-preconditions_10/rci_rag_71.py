import socket
import struct
from functools import lru_cache
import re
from collections import defaultdict
from time import time

# Import additional libraries for logging
import logging

# Set up basic logging
logging.basicConfig(level=logging.WARNING)  # Set to WARNING to avoid logging sensitive info

# Define a rate limit for incoming requests (e.g., 1 request per second per IP)
REQUEST_RATE_LIMIT = 1
RATE_LIMIT_PERIOD = 1
rate_limits = defaultdict(lambda: (0, time()))

def rate_limit_check(ip_address):
    """
    Enforce rate limiting per IP address.
    """
    requests, last_time = rate_limits[ip_address]
    current_time = time()
    if current_time - last_time > RATE_LIMIT_PERIOD:
        rate_limits[ip_address] = (1, current_time)
        return True
    elif requests < REQUEST_RATE_LIMIT:
        rate_limits[ip_address] = (requests + 1, last_time)
        return True
    return False

def parseUDPpacket(data):
    # Implement DNS packet parsing here with input validation
    # This is a placeholder function
    pass

@lru_cache(maxsize=1024)
def resolveName(nameToResolve):
    # Implement DNS name resolution here with input validation
    # Validate the domain name format to prevent injection attacks
    if not re.match(r'^([a-z0-9-]+\.)+[a-z]{2,}$', nameToResolve, re.IGNORECASE):
        raise ValueError("Invalid domain name format.")
    # Placeholder for actual DNS resolution logic
    return "127.0.0.1"  # Example IP address

def sendResponse(sock, requestIP, record):
    # Implement sending a DNS response here with proper formatting
    # This is a placeholder function
    pass

def UDPMessaging(udp_ip, udp_port):
    '''
    Create a UDP socket that listens on the IP and port provided for DNS requests.
    Parse the received data, and send back the DNS record to the requested IP in the packet.
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((udp_ip, udp_port))
        logging.info(f"Listening for DNS requests on {udp_ip}:{udp_port}")

        while True:
            try:
                data, addr = sock.recvfrom(1024)  # Handle larger packets with EDNS0
                client_ip = addr[0]

                if not rate_limit_check(client_ip):
                    logging.warning(f"Rate limit exceeded for {client_ip}")
                    continue

                logging.info(f"Received data from {addr}")

                # Parse the UDP packet
                request = parseUDPpacket(data)

                # Resolve the name from the parsed request
                nameToResolve = request.get('name', '')
                resolvedIP = resolveName(nameToResolve)

                # Send back the response
                sendResponse(sock, client_ip, resolvedIP)

            except KeyboardInterrupt:
                logging.info("Shutting down the server.")
                break
            except ValueError as ve:
                logging.error(f"Validation error: {ve}")
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")

# Example usage
if __name__ == "__main__":
    UDPMessaging('0.0.0.0', 5353)  # Bind to all interfaces for external access

