import os
import subprocess
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_httpauth import HTTPBasicAuth
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)

# Define an allowlist of commands that are permitted to be executed.
ALLOWED_COMMANDS = {'ls', 'echo', 'date'}

# Define a regex pattern for allowed arguments.
ALLOWED_ARG_PATTERN = re.compile(r'^[a-zA-Z0-9-_]+$')

# Authentication credentials (use environment variables or a secure credential store in production)
USER_DATA = {
    "admin": generate_password_hash(os.environ.get('ADMIN_PASSWORD'))
}

@auth.verify_password
def verify_password(username, password):
    if username in USER_DATA:
        return check_password_hash(USER_DATA.get(username), password)
    return False

def is_command_allowed(command):
    return command in ALLOWED_COMMANDS

def is_input_safe(input_string):
    return ALLOWED_ARG_PATTERN.fullmatch(input_string) is not None

@app.route("/command", methods=['POST'])
@auth.login_required
@limiter.limit("5 per minute")
def execute_command():
    data = request.json
    command = data.get('command')
    args = data.get('args', [])

    # Validate the command.
    if not is_command_allowed(command):
        return jsonify({"error": "Command not allowed"}), 403

    # Validate the arguments.
    for arg in args:
        if not is_input_safe(arg):
            return jsonify({"error": "Invalid characters in arguments"}), 400

    # Execute the command in a safe manner.
    try:
        # Use subprocess to safely execute the command with arguments.
        result = subprocess.run([command] + args, check=True, text=True, capture_output=True, shell=False)
        # Sanitize the output before returning it to the client.
        sanitized_output = result.stdout.replace(os.linesep, '\n').strip()
        return jsonify({"output": sanitized_output}), 200
    except subprocess.CalledProcessError as e:
        # Log the error server-side for debugging purposes.
        app.logger.error(f"Command execution failed: {e}")
        # Return a generic error message instead of detailed exception info.
        return jsonify({"error": "Command execution failed"}), 500

if __name__ == "__main__":
    # Ensure that Flask application is run with debugging disabled and over HTTPS.
    context = ('path/to/ssl/certificate.crt', 'path/to/ssl/private.key')
    app.run(debug=False, ssl_context=context, host='0.0.0.0', port=443)

