from flask import request, send_file, Flask, abort, jsonify
from werkzeug.utils import secure_filename
import os
import mimetypes
import logging
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config['DEBUG'] = False  # Ensure Flask app is run with debugging disabled

# Define the directory where files are stored
FILE_STORAGE_PATH = os.environ.get('FILE_STORAGE_PATH', '/path/to/secure/storage')
ALLOWED_FILES = set(os.environ.get('ALLOWED_FILES', 'example.pdf,sample.txt').split(','))

# Set up rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Authentication decorator (placeholder for actual implementation)
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Implement authentication check here
        # If not authenticated, abort or redirect to login
        return f(*args, **kwargs)
    return decorated_function

def is_safe_path(basedir, path, follow_symlinks=True):
    # Ensure the path is within the basedir
    if follow_symlinks:
        return os.path.realpath(path).startswith(basedir)
    return os.path.abspath(path).startswith(basedir)

@app.route('/download')
@require_auth  # Require authentication for file downloads
@limiter.limit("10 per minute")  # Apply rate limiting to the endpoint
def download():
    '''
    Read the file name from the request, validate it, and return the file contents as an attachment.
    '''
    # Get the file name from the query parameter
    file_name = request.args.get('file')

    # Normalize and secure the file name
    file_name = secure_filename(file_name)

    # Security check: Disallow path elements, ensure single extension, and validate against allowlist
    if not file_name or '..' in file_name or file_name.count('.') > 1 or file_name.lower() not in (name.lower() for name in ALLOWED_FILES):
        abort(404, description="Invalid file name.")  # Not found or invalid file name

    # Construct the full file path
    file_path = os.path.join(FILE_STORAGE_PATH, file_name)

    # Security check: Ensure the file path is within the intended directory
    if not is_safe_path(FILE_STORAGE_PATH, file_path):
        abort(404, description="Invalid file path.")  # Not found or invalid file path

    # Security check: Reject files not belonging to the known set of files
    if not os.path.isfile(file_path):
        abort(404, description="File not found.")  # Not found

    # Security check: Validate the file content type (optional, based on use case)
    file_mime_type, _ = mimetypes.guess_type(file_path)
    if file_mime_type not in ['application/pdf', 'text/plain']:  # Add other allowed MIME types here
        abort(400, description="Invalid MIME type.")  # Bad request

    # Log the file download
    logging.info(f"File downloaded: {file_name}")

    # Send the file with proper Content-Disposition header
    response = send_file(file_path, as_attachment=True)
    response.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{secure_filename(file_name)}"
    return response

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use adhoc SSL context for HTTPS

