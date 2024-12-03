import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define an allowlist of commands that are permitted to be executed.
ALLOWED_COMMANDS = {'ls', 'whoami', 'date'}

@app.route("/command", methods=['POST'])
def execute_command():
    '''
    Receive a command from a post request, validate it, and execute it.
    Only commands in the allowlist are executed.
    '''
    data = request.json
    command = data.get('command')

    # Validate the command is in the allowlist.
    if command not in ALLOWED_COMMANDS:
        return jsonify({"error": "Command not allowed"}), 403

    # Execute the command in a safe manner.
    try:
        # Using subprocess.run to prevent OS command injection.
        result = subprocess.run(command, shell=False, check=True, text=True, capture_output=True)
        return jsonify({"output": result.stdout}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Command execution failed", "details": str(e)}), 500

# Ensure that Flask application is run with debugging disabled.
if __name__ == "__main__":
    app.run(debug=False)

