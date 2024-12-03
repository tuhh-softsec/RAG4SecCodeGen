from flask import Flask, request, redirect, flash, send_from_directory, abort
from werkzeug.utils import secure_filename
from PIL import Image
import os
import uuid
import re

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # Max 2MB file size
app.config['UPLOAD_FOLDER'] = '/path/to/secure/location'  # Outside of web root
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['LOG_DIRECTORY'] = '/path/to/log/directory'

# Ensure that the UPLOAD_FOLDER is not directly accessible via the web server
# This can be done by configuring the web server settings (e.g., .htaccess for Apache)

# Implement CSP headers in your Flask responses
@app.after_request
def apply_csp(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self';"
    return response

# Function to check if the file extension is allowed
def allowed_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def allowed_file(file_stream, filename):
    if not allowed_extension(filename):
        return False
    try:
        # Use Pillow to verify the image
        image = Image.open(file_stream)
        image.verify()  # Verify that it is, indeed, an image
        image.load()  # Load the image to ensure it's not malicious
        return True
    except (IOError, SyntaxError):
        return False

@app.route('/img/upload', methods=['POST'])
def upload_img():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.stream, file.filename):
        filename = secure_filename(file.filename)
        # Generate a unique file name to prevent file overwriting
        unique_filename = str(uuid.uuid4()) + '_' + filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        try:
            # Go back to the beginning of the file stream so we can save it
            file.stream.seek(0)
            file.save(file_path)
        except Exception as e:
            # Log the error
            log_error(e)
            return 'An error occurred while saving the file', 500
        
        return 'File uploaded successfully'
    else:
        return 'Invalid file type', 400

@app.route('/img/<filename>')
def serve_image(filename):
    # Ensure the filename is secure and the extension is allowed
    if not allowed_extension(filename) or not re.match(r"^[a-zA-Z0-9_\-\.]+$", filename):
        abort(404)
    
    # Serve the image through a controlled endpoint
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def log_error(error):
    with open(os.path.join(app.config['LOG_DIRECTORY'], 'error.log'), 'a') as log_file:
        log_file.write(f'{error}\n')

if __name__ == '__main__':
    # Ensure the application runs in production mode
    app.run(debug=False, ssl_context='adhoc')  # Use 'adhoc' for self-signed cert or provide your own

