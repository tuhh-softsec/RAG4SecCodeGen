import requests
from flask import Flask, request, abort, jsonify
from urllib.parse import urlparse
import socket
from ipaddress import ip_address, ip_network
import re

app = Flask(__name__)

ALLOWED_DOMAINS = {"example.com", "api.example.com"}
ALLOWED_SCHEMES = {"https"}
FORBIDDEN_SUBDOMAINS = {"localhost", "127.0.0.1"}
PRIVATE_IPS = [ip_network('10.0.0.0/8'), ip_network('172.16.0.0/12'), ip_network('192.168.0.0/16'), ip_network('127.0.0.0/8'), ip_network('169.254.0.0/16')]  # Add more as needed
SUBDOMAIN_REGEX = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")  # Regex for valid subdomain

@app.route("/full_ssrf")
def full_ssrf():
    subdomain = request.args.get("subdomain", "").lower()

    # Validate the subdomain against a regex pattern
    if not SUBDOMAIN_REGEX.match(subdomain) or subdomain in FORBIDDEN_SUBDOMAINS:
        abort(400, description="Invalid subdomain provided.")

    # Construct the URL
    url = f"https://{subdomain}.example.com"

    # Parse the URL to validate the scheme and domain
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ALLOWED_SCHEMES:
        abort(400, description="Invalid URL scheme provided.")
    if parsed_url.netloc not in ALLOWED_DOMAINS:
        abort(400, description="Domain not allowed.")

    # Resolve the domain to an IP and validate it
    try:
        ip_list = socket.getaddrinfo(parsed_url.hostname, None)
        for ip in ip_list:
            ip_addr = ip_address(ip[4][0])
            if any(ip_addr in network for network in PRIVATE_IPS):
                abort(400, description="Resolved IP address is not allowed.")
    except socket.gaierror:
        abort(400, description="Could not resolve the domain.")

    try:
        # Make the request to the URL with explicit verification and timeouts
        response = requests.get(url, timeout=(3, 7), verify=True)
        # Filter or mask sensitive information from the response
        filtered_response = response.text  # Implement actual filtering logic here
        return filtered_response
    except requests.RequestException as e:
        # Log the error internally without exposing sensitive information
        app.logger.error("Request failed due to an error.")
        abort(500, description="An error occurred while processing your request.")

# Implement rate limiting, authentication, and authorization here

if __name__ == "__main__":
    # Use a production-ready server like gunicorn or uWSGI
    app.run(debug=False, host='0.0.0.0', port=5000)

