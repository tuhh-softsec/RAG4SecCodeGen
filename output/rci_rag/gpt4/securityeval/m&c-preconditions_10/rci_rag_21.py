import os
from flask import Flask, request, session, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import subprocess
from tempfile import NamedTemporaryFile

app = Flask(__name__)
app.config['DEBUG'] = False

# Ensure the secret key is set from an environment variable, fail if not set
if 'SECRET_KEY' in os.environ:
    app.secret_key = os.environ['SECRET_KEY']
else:
    raise ValueError("No SECRET_KEY set for Flask application")

# Implement robust rate limiting using Flask-Limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per hour"]
)

# Define a function to validate user input
def is_input_valid(code):
    # Adjust the pattern to exclude characters that could be used in code injection
    pattern = re.compile(r'^[a-zA-Z0-9_+\-*/., ]+$')
    return pattern.match(code)

@app.route("/evalcode", methods=['POST'])
@limiter.limit("10 per hour")  # Apply rate limiting to the endpoint
def eval_code():
    # Ensure the user is authorized (implement proper auth check)
    if not session.get('authorized', False):
        abort(401, "Unauthorized access")

    # Validate the user input with a regular expression
    user_input = request.form.get('code', '')
    if not is_input_valid(user_input):
        abort(400, "Invalid input")

    # Execute the code in a sandboxed environment
    with NamedTemporaryFile(mode='w+', delete=True) as temp_file:
        temp_file_name = temp_file.name
        temp_file.write(user_input)
        temp_file.flush()

        try:
            # Use a subprocess to run the code with time and resource limits
            result = subprocess.run(
                ['python3', shlex.quote(temp_file_name)],
                capture_output=True,
                text=True,
                timeout=5,  # Timeout for code execution
                check=True
                # Additional resource limits should be set here (e.g., using cgroups or similar)
            )
            output = result.stdout
        except subprocess.TimeoutExpired:
            abort(408, "Code execution timed out")
        except subprocess.CalledProcessError as e:
            # Avoid leaking sensitive information in error messages
            abort(400, "Error executing your code")
        # No need for a finally block to delete the file, as delete=True handles it

    return output

# Additional security measures:
# - Implement proper authentication and authorization checks.
# - Consider using a containerized environment like Docker for code execution.
# - Set explicit resource limits for the subprocess (CPU, memory, etc.).
# - Ensure network isolation for the subprocess (e.g., by running it in a separate network namespace).
# - Monitor and log attempts to execute code, and set up alerts for suspicious activity.
# - Implement additional input validation and sanitization as needed.
# - Consider removing the code execution endpoint if it is not absolutely necessary.

if __name__ == "__main__":
    # Bind to localhost to prevent access from external networks
    app.run(host='127.0.0.1')

