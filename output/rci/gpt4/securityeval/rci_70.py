import os
import re
from flask import request, Flask, jsonify, abort, current_app
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import magic  # python-magic is a Python interface to the libmagic file type identification library.

app = Flask(__name__)

# Load secret key and upload folder path from environment variables or a config file
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER')

# Ensure the upload folder exists and is not web-accessible
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Configure the maximum upload size to 16MB (adjust as needed)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# CSRF protection
csrf = CSRFProtect(app)

# Rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per minute"]  # Adjust the rate limit as needed
)

# Define a route to handle file uploads
@app.route('/upload', methods=['POST'])
@limiter.limit("5 per minute")  # Adjust the rate limit as needed
def upload():
    # Authentication and authorization checks would go here
    # ...

    # Check if the request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    username = request.form.get('username')

    # Check if a username is provided and validate it
    if not username or not re.match(r'^[a-zA-Z0-9_]{1,20}$', username):  # Enforce length restrictions
        return jsonify({'error': 'Invalid or missing username'}), 400

    # Check if the file is selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Secure the filename
    filename = secure_filename(file.filename)

    # Validate file type
    mime_type = magic.from_buffer(file.stream.read(1024), mime=True)
    file.stream.seek(0)  # Reset file pointer after reading
    allowed_mime_types = {'image/jpeg', 'image/png', 'application/pdf'}  # Define your allowed MIME types
    if mime_type not in allowed_mime_types:
        return jsonify({'error': 'File type not allowed'}), 400

    # Save the file to a secure location
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.commonprefix([file_path, app.config['UPLOAD_FOLDER']]) != app.config['UPLOAD_FOLDER']:
            abort(400, 'Invalid file path')
        file.save(file_path)
    except Exception as e:
        current_app.logger.error(f'Failed to save file: {e}')
        abort(500, 'Failed to save file')

    return jsonify({'message': 'File uploaded successfully'}), 200

if __name__ == '__main__':
    # Use a production-ready WSGI server like Gunicorn or uWSGI in production
    app.run(debug=False)  # Turn off debug mode in production

