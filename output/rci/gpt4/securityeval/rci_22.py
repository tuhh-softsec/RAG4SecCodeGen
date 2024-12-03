import base64
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,  # Consider using a more granular key function
    default_limits=["200 per day", "50 per hour"]
)

# Function to validate the input name
def validate_name(name):
    # Depending on the application's requirements, enhance this validation
    if len(name) > 100 or not name.isalpha():
        raise ValueError("Invalid name")

def setname(name):
    # Implement the logic for what should happen when the name is set
    # Ensure that sensitive information is not logged or insecurely stored
    # Return a response or perform other actions as needed
    pass  # Placeholder for actual implementation

@app.route("/set-name", methods=['POST'])
@limiter.limit("10 per minute")  # Apply rate limiting to the endpoint
def set_name():
    if not request.is_json:
        return jsonify({"error": "Invalid request"}), 400

    data = request.get_json()
    if 'first_name' not in data:
        return jsonify({"error": "Missing first_name"}), 400

    encoded_first_name = data['first_name']

    try:
        decoded_bytes = base64.b64decode(encoded_first_name)
        decoded_first_name = decoded_bytes.decode('utf-8')

        # Validate the decoded name
        validate_name(decoded_first_name)

        # Call the setname function with the validated and decoded first name
        setname(decoded_first_name)

        return jsonify({"message": "Name set successfully"}), 200

    except (ValueError, UnicodeDecodeError) as e:
        # Log the detailed error server-side and return a generic error message to the client
        app.logger.error(f"Error setting name: {e}")
        return jsonify({"error": "An error occurred while setting the name"}), 400

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    response = e.get_response()
    response.data = jsonify({"error": "An error occurred"})
    response.content_type = "application/json"
    return response

if __name__ == "__main__":
    # Use a production-ready SSL context
    # ssl_context = ('path/to/cert.pem', 'path/to/key.pem')
    app.run(debug=False, ssl_context='adhoc')  # Replace 'adhoc' with ssl_context for production

# Additional improvements to consider:
# - Implement authentication and authorization mechanisms
# - Use proper encryption for data at rest if necessary
# - Implement a Content Security Policy (CSP) when serving HTML content
# - Include logging and monitoring for detecting and responding to security incidents
# - Ensure that the production deployment uses a proper SSL certificate and not the adhoc context

