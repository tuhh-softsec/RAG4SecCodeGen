import socket
import struct
import re
import time
from collections import defaultdict
from threading import Lock

# Constants
BUFFER_SIZE = 512  # Standard DNS packet size; adjust if using EDNS0
RATE_LIMIT = 100  # Example rate limit value, adjust as needed
RATE_LIMIT_WINDOW = 60  # Time window in seconds for rate limiting
MAX_PACKET_SIZE = 512  # Maximum allowed packet size to prevent memory issues

# Rate limiting dictionary with expiration
rate_limiting_dict = defaultdict(lambda: [0, time.time()])
rate_limiting_lock = Lock()  # Lock for thread-safe access to rate_limiting_dict

def is_valid_hostname(hostname):
    # Check if the hostname is a valid DNS hostname
    if len(hostname) > 255:
        return False
    if not re.match(r'^[a-z0-9-]+(\.[a-z0-9-]+)*$', hostname, re.IGNORECASE):
        return False
    return True

def parseUDPpacket(data):
    if len(data) > MAX_PACKET_SIZE:
        raise ValueError("Packet size exceeds maximum allowed limit")
    try:
        # Basic input validation
        name_to_resolve = data.decode('utf-8').strip()
        if not is_valid_hostname(name_to_resolve):
            raise ValueError("Invalid hostname")
        return name_to_resolve
    except UnicodeDecodeError:
        raise ValueError("Invalid UTF-8 data")

def resolveName(nameToResolve):
    # Implement your name resolution logic here
    # This is a placeholder implementation that simply echoes the name
    if not is_valid_hostname(nameToResolve):
        return None
    return f"Resolved record for {nameToResolve}"

def sendResponse(sock, requestIP, requestPort, record):
    if record is not None:
        # Implement your logic to send a response back to the request IP
        # This is a placeholder implementation
        response = record.encode('utf-8')
        sock.sendto(response, (requestIP, requestPort))
        # Removed sensitive information from logging

def rate_limited(addr):
    global rate_limiting_dict
    with rate_limiting_lock:
        ip, port = addr
        current_time = time.time()
        requests, last_reset = rate_limiting_dict[ip]

        # Reset rate limit counter if the time window has passed
        if current_time - last_reset > RATE_LIMIT_WINDOW:
            rate_limiting_dict[ip] = [0, current_time]
            requests = 0

        if requests >= RATE_LIMIT:
            return True
        rate_limiting_dict[ip][0] = requests + 1
        return False

def UDPMessaging(udp_ip, udp_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((udp_ip, udp_port))
        # Removed sensitive information from logging

        while True:
            try:
                data, addr = sock.recvfrom(BUFFER_SIZE)
                # Removed sensitive information from logging

                if rate_limited(addr):
                    # Removed sensitive information from logging
                    continue

                name_to_resolve = parseUDPpacket(data)
                record = resolveName(name_to_resolve)
                sendResponse(sock, addr[0], addr[1], record)

            except ValueError as ve:
                # Removed sensitive information from logging
            except KeyboardInterrupt:
                # Removed sensitive information from logging
                break
            except Exception as e:
                # Removed sensitive information from logging

if __name__ == "__main__":
    udp_ip = "0.0.0.0"  # Bind to all interfaces
    udp_port = 5353
    UDPMessaging(udp_ip, udp_port)

