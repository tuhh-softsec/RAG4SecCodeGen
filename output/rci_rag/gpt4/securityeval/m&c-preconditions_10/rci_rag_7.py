import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
app.config['DEBUG'] = False  # Ensure Flask is run with debugging disabled

# Define the allowed extensions for image files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Define the directory where images are stored as an absolute path
IMAGE_DIR = os.path.abspath('/path/to/your/images')

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Implement your authentication logic here (e.g., API token check)
        # If authentication fails, return a 401 Unauthorized response
        return f(*args, **kwargs)
    return decorated_function

# Authorization decorator
def require_permission(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Implement your authorization logic here (e.g., check user permissions)
        # If authorization fails, return a 403 Forbidden response
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/deleteImage/<filename>', methods=['DELETE'])
@require_auth
@require_permission
def delete_image(filename):
    filename = secure_filename(filename)

    if not allowed_file(filename):
        return jsonify({'error': 'File type not allowed'}), 400

    file_path = os.path.join(IMAGE_DIR, filename)
    file_path = os.path.realpath(file_path)

    if not file_path.startswith(IMAGE_DIR):
        return jsonify({'error': 'Invalid file path'}), 403

    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    try:
        os.remove(file_path)
        if os.path.exists(file_path):
            # Log the failed deletion attempt here
            return jsonify({'error': 'File could not be deleted'}), 500
        # Log the successful deletion attempt here
        return jsonify({'message': 'File deleted'}), 200
    except OSError as e:
        # Log the error here with a generic message for the client
        return jsonify({'error': 'An error occurred while deleting the file'}), 500

if __name__ == '__main__':
    # Use a production-ready server like Gunicorn or uWSGI in production
    app.run()

