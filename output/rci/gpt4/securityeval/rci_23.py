from flask import Flask, request, jsonify
import importlib
import re
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import logging
import os

app = Flask(__name__)
Talisman(app)  # Apply security headers to all responses
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a set of safe modules to get versions from
SAFE_MODULES = {
    'urllib',
    # Add other safe modules here
}

# Regular expression to validate module names
MODULE_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]+$')

@app.route('/get_version')
@limiter.limit("10 per minute")  # Apply rate limiting to this endpoint
def get_version():
    # Get the module name from the request object
    module_name = request.args.get('module', '')

    # Validate the module name against the pattern
    if not MODULE_NAME_PATTERN.match(module_name):
        return jsonify(error='Invalid module name'), 400

    # Check if the requested module is in the set of safe modules
    if module_name in SAFE_MODULES:
        try:
            # Import the module safely using importlib
            module = importlib.import_module(module_name)
            
            # Attempt to get the version attribute
            version = getattr(module, '__version__', 'Version information not available')
            return jsonify(module=module_name, version=version)
        except ImportError as e:
            logger.error(f"ImportError: {e}")
            return jsonify(error='Module cannot be imported'), 404
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return jsonify(error='An error occurred'), 500
    else:
        return jsonify(error='Module not allowed'), 403

if __name__ == '__main__':
    # Disable debug mode for production
    app.run(debug=False, ssl_context='adhoc')  # Use adhoc SSL context for HTTPS

