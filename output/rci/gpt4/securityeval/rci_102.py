from flask import Flask, request, jsonify
from defusedxml.ElementTree import parse
import re

app = Flask(__name__)

# Implement rate limiting (example using Flask-Limiter)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/user', methods=['GET'])
@limiter.limit("5 per minute")  # Rate limit for this endpoint
def user_locations():
    try:
        # Parse the XML securely using defusedxml
        tree = parse('users.xml')
        root = tree.getroot()

        # Retrieve the username from the request args and sanitize it
        username = request.args.get('username', '')

        # Ensure that the username is a plain text string and check its length
        if not re.match(r'^[a-zA-Z0-9]{1,30}$', username):
            return jsonify({"error": "Invalid input"}), 400

        # Use a parameterized XPath query to avoid string interpolation
        xpath_query = ".//user[@name=$username]/location"
        locations = root.findall(xpath_query, namespaces={'username': username})

        # Extract the location text and return it as a JSON response
        location_list = [location.text for location in locations]
        return jsonify(location_list)

    except Exception as e:
        # Log the exception details server-side (example using logging module)
        app.logger.error(f"Unhandled exception: {e}")
        # Return a generic error message to the client
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    # Run the application without debug mode in production
    app.run(debug=False, ssl_context='adhoc')  # Enable SSL/TLS

# Additional security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

