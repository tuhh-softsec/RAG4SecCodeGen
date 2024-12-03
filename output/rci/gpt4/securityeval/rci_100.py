import os
from flask import Flask, request, send_from_directory, abort, safe_join, after_this_request
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import mimetypes
from logging.handlers import RotatingFileHandler
import logging

app = Flask(__name__)

# Define the directory where your downloadable files are located
DOWNLOAD_FOLDER = '/path/to/your/downloadable/files'
# Ensure that this path is not publicly accessible directly through the web server

# Configure logging
logging.basicConfig(filename='error.log', level=logging.WARNING)
file_handler = RotatingFileHandler('error.log', maxBytes=1024 * 1024 * 100, backupCount=20)
app.logger.addHandler(file_handler)

# Set up rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]  # Adjust the rate limit as needed
)

# Security headers
@app.after_request
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.route('/download')
@limiter.limit("3 per minute")  # Adjust the rate limit as needed for this endpoint
def download():
    '''
    Get the file name from the request and parse the name to get the file path.
    Send the file to the client as an attachment.
    '''
    # Authentication and authorization checks should be implemented here

    # Get the file name from the query parameter
    file_name = request.args.get('file')

    # Validate and sanitize the file_name to prevent directory traversal and other attacks
    if file_name is None:
        abort(400, "No file specified.")

    # Use secure_filename to prevent directory traversal attacks
    file_name = secure_filename(file_name)

    # Construct the full file path
    try:
        file_path = safe_join(DOWNLOAD_FOLDER, file_name)
    except ValueError:
        abort(400, "Invalid file path.")

    # Resolve any symlinks and check that the file is within the DOWNLOAD_FOLDER
    real_file_path = os.path.realpath(file_path)
    if not real_file_path.startswith(os.path.realpath(DOWNLOAD_FOLDER)):
        abort(403, "Access denied.")

    # Check if file exists and is a file (not a directory)
    if not os.path.isfile(real_file_path):
        abort(404, "File not found.")

    # Determine the correct MIME type for the file
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'

    # Send the file as an attachment with the correct MIME type
    response = send_from_directory(DOWNLOAD_FOLDER, file_name, as_attachment=True, mimetype=mime_type)

    # Ensure the Content-Disposition header is safe
    response.headers.set('Content-Disposition', 'attachment', filename=file_name)

    return response

if __name__ == '__main__':
    # Use a production-ready WSGI server like Gunicorn or uWSGI in production
    # Ensure that the application is running over HTTPS with a valid SSL certificate in production
    app.run(ssl_context='adhoc')

