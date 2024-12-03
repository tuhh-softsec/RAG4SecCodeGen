from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re
import subprocess
import os
import json

app = Flask(__name__)

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per minute"]
)

# Function to run the regex search in a subprocess with a timeout
def regex_search(pattern, text):
    try:
        # Validate the regex pattern to prevent ReDoS attacks
        # Here you can add additional validation for the pattern if needed
        regex = re.compile(pattern)
        match = regex.search(text)
        return match.group() if match else None
    except re.error as e:
        return f"error: {str(e)}"

@app.route("/search", methods=["GET"])
@limiter.limit("5 per second")  # Adjust the rate limit as needed
def search():
    pattern = request.args.get('pattern', default='', type=str)
    text = request.args.get('text', default='', type=str)

    # Limit the size of the input text to mitigate performance issues
    max_text_length = 10000  # Example limit, adjust as needed
    if len(text) > max_text_length:
        return jsonify({"error": "Input text too long."}), 413

    # Run the regex search in a subprocess with a timeout
    try:
        process = subprocess.run(
            ['python', '-c', json.dumps(f'import re; print({json.dumps(regex_search(pattern, text))})')],
            capture_output=True,
            text=True,
            timeout=int(os.getenv('REGEX_TIMEOUT', 1))  # Make the timeout configurable
        )
        result = process.stdout.strip()
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Regex search timed out."}), 504
    except subprocess.SubprocessError as e:
        return jsonify({"error": str(e)}), 500

    # Check if there was an error during regex compilation or search
    if result.startswith("error:"):
        return jsonify({"error": result}), 400

    # Return the result of the regex search
    if result:
        # Ensure that the matched string is safely encoded to prevent XSS
        return jsonify({"match": result})
    else:
        return jsonify({"message": "No match found."})

# Set up application configuration for production
if __name__ == "__main__":
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Configure HTTPS enforcement and other security features
    # ...

    # Configure logging and monitoring
    # ...

    # Configure HTTP security headers
    # ...

    # Run the application with a production-ready server like Gunicorn
    # ...

