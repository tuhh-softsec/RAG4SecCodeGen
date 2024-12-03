from flask import Flask, request, escape, make_response
import logging
from werkzeug.exceptions import BadRequest

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Set the session cookie to HttpOnly
@app.after_request
def apply_http_only(response):
    response.headers["Set-Cookie"] = "HttpOnly; Secure"
    return response

# Specify encoding in the HTTP header
@app.before_request
def set_response_encoding():
    request.charset = 'utf-8'

@app.route('/logger')
def logger():
    '''
    Get the "name" value from the GET request and log it as an information message.
    '''
    # Validate the data in the request
    name = request.args.get('name', '')
    if not name.isalnum():
        raise BadRequest("Invalid input. Only alphanumeric characters are allowed.")

    # Escape special characters before writing the HTTP parameter back to the page
    safe_name = escape(name)

    # Log the safe, escaped name
    app.logger.info(f"Received name: {safe_name}")

    # Do not display inconsistent messages or sensitive information
    response = make_response("Name logged successfully", 200)
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    return response

if __name__ == '__main__':
    # Ensure that Flask application is run with debugging disabled
    app.run(debug=False)

