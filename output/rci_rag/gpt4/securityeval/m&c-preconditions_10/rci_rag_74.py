from flask import Flask, request, redirect, flash, abort, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
import magic
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config['DEBUG'] = False  # Disable Flask debugging in production
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', '/path/to/uploads')  # Use environment variable for configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')  # Use an environment variable for a persistent secret key

csrf = CSRFProtect(app)  # Enable CSRF protection
limiter = Limiter(app, key_func=get_remote_address)  # Enable rate limiting

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Set up logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def is_pdf(filestream):
    mime = magic.from_buffer(filestream.read(1024), mime=True)
    filestream.seek(0)  # Reset file pointer after reading
    return mime == 'application/pdf'

@app.route('/pdf/upload', methods=['POST'])
@csrf.exempt  # Exempt this route from CSRF token requirement
@limiter.limit("10 per minute")  # Rate limit to 10 uploads per minute
def upload_pdf():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename) and is_pdf(file.stream):
        filename = secure_filename(file.filename)
        # Add a unique identifier to the filename to prevent overwrites
        unique_id = uuid.uuid4().hex
        filename = f"{unique_id}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        app.logger.info(f"File uploaded: {filepath}")  # Log the file upload
        return redirect(url_for('uploaded_file', filename=filename))
    else:
        flash('Invalid file type or content')
        abort(400)

@app.route('/pdf/view/<filename>')
def uploaded_file(filename):
    # Ensure the filename is secure and serve the file with attachment disposition
    filename = secure_filename(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# Add other routes and logic as needed

if __name__ == '__main__':
    # Use a proper SSL context in production, not 'adhoc'
    app.run(ssl_context=('cert.pem', 'key.pem'))  # Replace with paths to your actual SSL certificate and key files

