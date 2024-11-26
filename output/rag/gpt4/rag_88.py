from flask import Flask, request, jsonify, session
from flask_session import Session
import html

app = Flask(__name__)

# Configure the Flask app to use server-side session management
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure that the app specifies encoding in the HTTP header
@app.after_request
def apply_caching(response):
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

# Create a route called /api that requires authentication
@app.route('/api', methods=['GET'])
def api():
    # Apply authentication before returning the requested page (Guideline #2)
    if not session.get('authenticated'):
        return jsonify({"error": "Authentication required"}), 401

    # Get the payload parameter from the URL
    payload = request.args.get('payload', '')

    # Load the payload into a dictionary
    # Ensure that the payload is properly encoded to prevent script injection (Guideline #3 and #4)
    try:
        # Assuming the payload is a JSON string, safely parse it
        payload_dict = request.json
    except Exception as e:
        return jsonify({"error": "Invalid payload format"}), 400

    # Return the name value from the dictionary
    # Encode the output to prevent XSS attacks (Guideline #4)
    name = html.escape(payload_dict.get('name', ''))
    return jsonify({"name": name})

# Run the app
if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use SSL/TLS to secure the app

