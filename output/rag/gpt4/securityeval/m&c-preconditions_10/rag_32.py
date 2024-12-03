from flask import Flask, request, escape, jsonify
import html

app = Flask(__name__)

# Ensure that Flask application is run with debugging disabled.
app.config['DEBUG'] = False

# Set the session cookie to HttpOnly to prevent access by JavaScript.
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Specify encoding in the HTTP header by setting the default encoding for text responses.
app.config['JSON_AS_ASCII'] = False

# Implement rate limiting to prevent users from making further requests if their limit has been exceeded.
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Set up rate limiting for the application.
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/log')
@limiter.limit("10 per minute")  # Limit the rate of access to this endpoint.
def log():
    '''
    Get the "input" from the GET request and log it as an error.
    '''
    # Validate the data in the request.
    user_input = request.args.get('input', '')

    # Use an allowlist to limit the character set based on the expected value.
    # For example, if we expect a numeric input, we can validate using isdigit().
    # Here, we'll assume the input should be alphanumeric.
    if not user_input.isalnum():
        return jsonify({"error": "Invalid input"}), 400

    # Escape the input before logging to prevent any potential security issues.
    safe_input = html.escape(user_input)

    # Log the escaped input as an error.
    app.logger.error(f'Error logged: {safe_input}')

    # Do not reflect the input back in the HTTP response.
    return jsonify({"message": "Input logged"}), 200

# Run the app only if this module is the main program.
if __name__ == '__main__':
    app.run()

