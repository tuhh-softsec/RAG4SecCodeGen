import os
import io
import hashlib
import binascii
from flask import Flask, request, redirect, abort, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
from PIL import Image
from functools import wraps
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

app = Flask(__name__)

# Configure logging to avoid sensitive information
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure Flask is run with debugging disabled in production
app.config['DEBUG'] = False

# Define the allowed extensions for images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Define the path to store uploaded images outside of the web document root
UPLOAD_FOLDER = '/path/to/secure/location/pictures'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define maximum file size (e.g., 2MB)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

# Initialize rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["60 per minute"]
)

# Initialize HTTP Basic Auth
auth = HTTPBasicAuth()

# Replace with your actual method to validate username and password
@auth.verify_password
def verify_password(username, password):
    # Here you should retrieve and verify the hashed password
    # For example, using environment variables:
    stored_password_hash = os.environ.get('USER_PASSWORD_HASH')
    salt = os.environ.get('USER_SALT')
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return username == os.environ.get('USER_NAME') and binascii.hexlify(pwdhash) == stored_password_hash

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(stream):
    try:
        Image.open(stream).verify()
        return True
    except Exception as e:
        logging.error(f"Image validation error: {e}")
        return False

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = jsonify({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.route('/img/upload', methods=['POST'])
@auth.login_required
@limiter.limit("10 per minute")  # Adjust rate limit as needed
def upload_img():
    if 'file' not in request.files:
        abort(400, description="No file part in the request.")

    file = request.files['file']

    if file.filename == '':
        abort(400, description="No selected file.")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Prevent directory traversal
        if '..' in filename or filename.startswith('/'):
            abort(400, description="Invalid filename.")

        # Generate a unique filename to prevent race conditions and file overwriting
        unique_filename = hashlib.sha256((filename + str(os.urandom(60))).encode('utf-8')).hexdigest()

        # Check content type
        content_type = file.content_type
        if content_type not in ['image/png', 'image/jpeg', 'image/gif']:
            abort(400, description="Invalid content type.")

        file.stream.seek(0)
        if not validate_image(file.stream):
            abort(400, description="Invalid image content.")

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.stream.seek(0)
        file.save(file_path)

        logging.info(f"File {filename} uploaded successfully as {unique_filename}.")
        return jsonify(message='File successfully uploaded'), 200
    else:
        abort(400, description="Invalid file extension or file not provided.")

if __name__ == '__main__':
    # Use a production-ready SSL context
    context = ('cert.pem', 'key.pem')
    app.run(ssl_context=context)

