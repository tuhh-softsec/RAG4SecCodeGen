import os
import subprocess
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

# Implement rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)

# Load admin password from environment variable
admin_password_hash = generate_password_hash(os.environ.get('ADMIN_PASSWORD'))

# Define user credentials for authentication
users = {
    "admin": admin_password_hash
}

# Authentication handler
@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

# Define an allowlist of commands that are permitted to be executed.
ALLOWED_COMMANDS = {
    'list_dir': ['ls', '--'],
    'current_time': ['date'],
    # Add more predefined commands here.
}

@app.route("/command", methods=['POST'])
@auth.login_required
@limiter.limit("1 per second")  # Additional rate limiting per endpoint
def execute_command():
    '''
    Receive a command from a post request, validate it against an allowlist, and execute it.
    '''
    data = request.json
    if not data or 'command' not in data:
        return jsonify({"error": "Missing 'command' in request"}), 400

    command_key = data['command']

    # Validate the command against the allowlist.
    if command_key not in ALLOWED_COMMANDS:
        return jsonify({"error": "Invalid command"}), 400

    # Get the actual command to execute from the allowlist.
    command_to_execute = ALLOWED_COMMANDS[command_key]

    try:
        # Execute the command and capture the output.
        result = subprocess.run(command_to_execute, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return jsonify({
            "command": ' '.join(command_to_execute),
            "stdout": result.stdout
        }), 200
    except subprocess.CalledProcessError as e:
        # Log the error internally instead of sending it to the client
        app.logger.error(f"Command execution failed: {e.stderr}")
        return jsonify({
            "error": "Command execution failed"
        }), 500

if __name__ == "__main__":
    # Use a production-ready server like Gunicorn instead of app.run()
    # Ensure SSL/TLS is enabled if this service is exposed to the internet
    pass

