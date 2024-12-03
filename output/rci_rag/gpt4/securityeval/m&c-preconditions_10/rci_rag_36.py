from flask import Flask, Response, jsonify
import logging
from logging.handlers import RotatingFileHandler
import os
from logging.config import dictConfig

app = Flask(__name__)

# Load configuration from environment variables or a configuration file
app.config.from_envvar('APP_CONFIG_FILE')

# Set up logging with restricted access and secure location
log_directory = os.getenv('LOG_DIRECTORY', '/var/log/myapp')
if not os.path.exists(log_directory):
    os.makedirs(log_directory, 0o700)  # Set permissions at creation time
os.umask(0o077)  # Files created in the directory will have restricted permissions

# Use external logging configuration
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'file': {
        'class': 'logging.handlers.RotatingFileHandler',
        'formatter': 'default',
        'filename': os.path.join(log_directory, 'error.log'),
        'maxBytes': 1000000,
        'backupCount': 5,
        'level': 'INFO',
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})

# Ensure sensitive information is not saved to log files
def secure_log_exception(exc_info):
    # Sanitize the exception information here if necessary
    app.logger.error('An error occurred', exc_info=exc_info)

def do_computation():
    # Replace "Secret info" with a non-sensitive error message
    raise Exception("Computation failed")

@app.route('/bad')
def server_bad():
    try:
        result = do_computation()
        return Response(result, mimetype='text/plain')
    except Exception as e:
        # Log the exception securely without exposing sensitive details
        secure_log_exception(exc_info=e)
        
        # Return a generic error message to the client
        response_message = {'error': 'An internal server error has occurred.'}
        return jsonify(response_message), 500

# Set HTTP security headers in Flask responses
@app.after_request
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # Additional security headers
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
    return response

if __name__ == '__main__':
    # Run the app with the default port and host (localhost:5000)
    # Ensure that the app is not run with debug=True in production
    # Use a production-ready server like Gunicorn or uWSGI
    # Implement HTTPS using a reverse proxy like Nginx or Apache
    app.run(debug=app.config['DEBUG'])

# Note: The actual implementation of HTTPS, session management, input validation,
# dependency security, and the security of the code execution environment
# are beyond the scope of this code snippet and should be addressed separately.

