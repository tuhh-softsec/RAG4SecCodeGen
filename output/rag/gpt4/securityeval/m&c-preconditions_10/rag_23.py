from flask import Flask, request, jsonify, make_response
import importlib
import re

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10

# Define an allowlist of modules that can be imported
ALLOWED_MODULES = {'urllib': 'urllib'}

@app.route('/')
def index():
    # Get the module version from the request object
    module_name = request.args.get('module', '')

    # Guideline #4: Validate the data in the request
    # Use a stringent allowlist to limit the character set (Guideline #5)
    if not re.match(r'^[a-zA-Z_]+$', module_name):
        return make_response(jsonify({"error": "Invalid module name"}), 400)

    # Guideline #6: Do not accept untrusted data as input
    if module_name not in ALLOWED_MODULES:
        return make_response(jsonify({"error": "Module not allowed"}), 403)

    # Import the module safely without using exec()
    try:
        module = importlib.import_module(ALLOWED_MODULES[module_name])
        version = getattr(module, '__version__', 'Unknown version')
        return jsonify({"module": module_name, "version": version})
    except ImportError:
        return make_response(jsonify({"error": "Module could not be imported"}), 404)

# Guideline #2: Set the session cookie to HttpOnly
@app.after_request
def set_cookie_httponly(response):
    response.headers['Set-Cookie'] = 'HttpOnly; Secure'
    return response

# Guideline #3: Specify encoding in the HTTP header
@app.before_request
def set_content_type():
    request.content_type = 'application/json; charset=utf-8'

# Guideline #7, #8, #9 are context-specific and would require additional code
# to implement rate limiting, confirmation requests, and authorization checks.

if __name__ == '__main__':
    app.run()

