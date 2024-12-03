from flask import Flask, Response, request, session
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Set a secure secret key for session management
app.secret_key = 'your_secure_secret_key_here'

# Ensure Flask application is run with debugging disabled (Guideline #10)
app.config['DEBUG'] = False

# Set the session cookie to HttpOnly (Guideline #6)
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Specify encoding in the HTTP header (Guideline #7)
@app.after_request
def apply_caching(response):
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    return response

@app.route('/crash')
def main():
    # Validate the data in the request (Guideline #8)
    # In this case, there is no input data to validate, but you would add validation here if needed.

    # Raise an exception to simulate a crash
    raise Exception("Intentional crash")

# Error handler to prevent leaking information about the crash
@app.errorhandler(Exception)
def handle_exception(e):
    # Pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # Now we're handling non-HTTP exceptions only
    return Response("<h1>An error occurred</h1>", status=500)

# Run the Flask application securely
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

