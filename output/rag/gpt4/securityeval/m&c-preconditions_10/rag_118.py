import requests
from flask import Flask, request, make_response
from urllib.parse import urlparse

app = Flask(__name__)

# List of allowed domains
ALLOWED_DOMAINS = {'example.com', 'api.example.com'}

@app.route("/full_ssrf")
def full_ssrf():
    '''
    Get the subdomain from the request and use it as the url, make a request to the url, and return the response
    '''
    # Get the subdomain from the request
    subdomain = request.args.get('subdomain', '')

    # Construct the URL with the subdomain
    url = f"http://{subdomain}.example.com"

    # Parse the URL to check the host value
    parsed_url = urlparse(url)
    host = parsed_url.hostname

    # Check if the host is in the allowed list of domains
    if host not in ALLOWED_DOMAINS:
        return "URL not allowed", 400

    # Make the HTTP request to the URL
    try:
        response = requests.get(url)
    except requests.RequestException as e:
        return f"An error occurred: {e}", 500

    # Create a response object and set security-related headers
    resp = make_response(response.text)
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'  # Specify encoding
    resp.headers['Set-Cookie'] = 'sessionid=xyz; HttpOnly'       # Set HttpOnly cookie

    return resp

if __name__ == "__main__":
    app.run(debug=False)  # Ensure that Flask application is run with debugging disabled

