from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import yaml
from yaml.loader import SafeLoader
import os
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Load configuration from environment variables or configuration file
app.config.from_envvar('YOUR_APPLICATION_SETTINGS')

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per minute"]
)

# Define a route to parse YAML data
@app.route('/yaml', methods=['POST'])
@limiter.limit("5 per second")  # Apply rate limiting to the endpoint
def yaml_load():
    '''
    Get YAML data from request, parse it using safe_load, and return it.
    '''
    # Check the Content-Type of the incoming request
    content_type = request.headers.get('Content-Type', '').lower()
    if not content_type.startswith('application/x-yaml'):
        return jsonify({"error": "Unsupported Content-Type"}), 415

    # Get the raw YAML data from the request
    yaml_data = request.data

    # Check if there's data to parse and if it's not too large
    max_size = 1024 * 1024  # 1 MB
    if not yaml_data:
        return jsonify({"error": "No YAML data provided"}), 400
    elif len(yaml_data) > max_size:
        return jsonify({"error": "YAML data too large"}), 413

    try:
        # Parse the YAML data safely
        parsed_data = yaml.load(yaml_data, Loader=SafeLoader)
        # Sanitize the parsed_data here before returning it
        # (Sanitization logic not shown here)
    except yaml.YAMLError as e:
        # Log the detailed error server-side
        app.logger.error(f"YAML parsing error: {e}")
        # Return a generic error message to the client
        return jsonify({"error": "Invalid YAML data"}), 400

    # Return the parsed data as JSON
    return jsonify(parsed_data)

# Configure proper server error handling
@app.errorhandler(500)
def handle_500(error):
    app.logger.error(f"Server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

# Other error handlers can be added here

# Run the application using a production WSGI server like Gunicorn
# Example command to run with Gunicorn: gunicorn -w 4 -b 0.0.0.0:443 myapp:app --certfile=/path/to/cert.pem --keyfile=/path/to/key.pem

# Remember to install Flask, PyYAML, Flask-Limiter, and Gunicorn if you haven't already:
# pip install Flask PyYAML Flask-Limiter gunicorn

# Additionally, ensure that you have a valid SSL certificate for production use and that you configure your reverse proxy (e.g., Nginx or Apache) to handle SSL/TLS termination and to set appropriate security headers.

