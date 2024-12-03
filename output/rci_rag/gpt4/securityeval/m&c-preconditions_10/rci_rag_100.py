import os
from flask import Flask, request, send_from_directory, abort, session, redirect, url_for
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)

# Load configuration from environment variables or a separate configuration file
app.config.from_pyfile('config.py')

# Define a decorator for access control
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'authenticated' not in session:
            # Redirect to login page or return an error
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/download', methods=['GET'])
@login_required  # Apply access control to the download endpoint
def download():
    filename = request.args.get('filename')
    if not filename:
        abort(404, description="No filename provided.")

    # Sanitize the filename first
    filename = secure_filename(filename)

    # Prevent directory traversal after sanitizing
    if '..' in filename or filename.startswith('/'):
        abort(400, description="Invalid filename.")

    if not allowed_file(filename):
        abort(400, description="File extension not allowed.")

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Validate that the resulting path is within the intended directory
    if not os.path.commonpath([file_path, app.config['UPLOAD_FOLDER']]) == os.path.realpath(app.config['UPLOAD_FOLDER']):
        abort(400, description="Invalid file path.")

    if not os.path.isfile(file_path):
        abort(404, description="File does not exist.")

    # Override the filename when sending the file to the client
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True, download_name='downloaded_file')

# Implement rate limiting, logging, CSP headers, and other security measures as needed

if __name__ == '__main__':
    # Run the app with SSL if HTTPS is not enforced by a reverse proxy
    app.run(ssl_context='adhoc' if not os.getenv('FLASK_RUN_FROM_CLI') else None)

# Additional security measures such as rate limiting and logging should be implemented according to your application's needs.

