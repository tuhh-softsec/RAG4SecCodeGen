import os
import base64
import json
from flask import Flask, request, abort, jsonify
from itsdangerous import URLSafeSerializer, BadData
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Load the secret key from an environment variable or configuration file
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
serializer = URLSafeSerializer(SECRET_KEY)

# Set up rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.route("/profile", methods=['GET'])
def profile():
    '''
    Get raw_data from request with utf-8 encoding and decode it with base64.
    Deserialize the decoded data, store it in a variable and return it.
    Ensure that the data is from a trusted source and handle exceptions.
    '''
    # Get the encoded data from the request args
    encoded_data = request.args.get('data', '')

    if not encoded_data:
        abort(400, description="No data provided.")

    try:
        # Decode the base64 encoded data
        decoded_data = base64.urlsafe_b64decode(encoded_data)

        # Verify the integrity and authenticity of the data
        data = serializer.loads(decoded_data)

        # Validate the structure and content of the deserialized data
        # (This step depends on the expected structure of your data)
        # For example, if you expect data to be a dictionary with certain keys:
        # if not all(key in data for key in ['expected_key1', 'expected_key2']):
        #     abort(400, description="Invalid data structure.")

        # Return the deserialized data (for demonstration purposes)
        # In a real application, you would likely do something with the data
        # rather than returning it directly.
        return jsonify(data)

    except BadData:
        abort(400, description="Invalid data provided.")
    except Exception as e:
        # Log the error internally and present a completely generic error message to the user
        app.logger.error(f"An unexpected error occurred: {e}")
        abort(500, description="An error occurred. Please try again later.")

if __name__ == "__main__":
    # Load configuration from environment variables or configuration files
    app.config.from_object('yourapplication.default_settings')
    app.config.from_envvar('YOURAPPLICATION_SETTINGS', silent=True)

    # Enforce HTTPS
    if not app.debug and not app.testing:
        from flask_talisman import Talisman
        Talisman(app)

    # Disable debug mode in production
    app.run(debug=False)

