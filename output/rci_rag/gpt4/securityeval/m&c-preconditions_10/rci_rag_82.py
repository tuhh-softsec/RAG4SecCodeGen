from flask import Flask, request, jsonify, make_response, session
import yaml
from functools import wraps

app = Flask(__name__)

# Set a secure and random secret key for the session
app.config['SECRET_KEY'] = 'a_secure_and_random_secret_key'

# Configure session cookies to be secure
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

# Disable Flask debugging mode
app.config['DEBUG'] = False

# Implement rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Use a more reliable key function for rate limiting if behind a proxy
def rate_limit_key_func():
    # Trust the X-Forwarded-For header if behind a proxy
    return session.get('user_id', request.headers.get('X-Forwarded-For', get_remote_address()))

limiter = Limiter(
    app,
    key_func=rate_limit_key_func,
    default_limits=["200 per day", "50 per hour"]
)

# Authorization decorator (dummy implementation)
def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Implement actual authorization logic here
        is_authorized = True
        if not is_authorized:
            return make_response(jsonify({"error": "Unauthorized"}), 403)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/yaml', methods=['POST'])
@limiter.limit("10 per minute")
@authorize
def yaml_load():
    # Validate the Content-Type header with a more flexible check
    if not request.content_type.startswith('application/x-yaml'):
        return make_response(jsonify({"error": "Invalid content type, application/x-yaml required"}), 400)

    try:
        yaml_data = yaml.safe_load(request.data)
    except yaml.YAMLError as e:
        app.logger.error(f"YAML parsing error: {e}")
        return make_response(jsonify({"error": "Invalid YAML data"}), 400)

    # Validate and sanitize the YAML data here before using it

    return jsonify(yaml_data)

# Set up proper logging
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

if __name__ == '__main__':
    # In production, use a proper SSL context with a valid certificate
    # app.run(ssl_context=('cert.pem', 'key.pem'))
    app.run(ssl_context='adhoc')  # Use ad-hoc SSL context for demonstration purposes only

