from flask import Flask, request, send_file, abort
import os
import re

app = Flask(__name__)

# Define the base directory where images are stored securely
# This should be outside of the web document root
IMAGE_BASE_PATH = '/path/to/secure/image/storage'

# Define allowed file extensions in a case-insensitive manner
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    # Check if the file has an allowed extension, case-insensitive
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_filename(filename):
    # Remove any path elements from the filename
    filename = os.path.basename(filename)
    # Use a secure function to strip any special characters or path manipulations
    return re.sub(r'[^a-zA-Z0-9_.-]', '', filename)

@app.route('/img')
def img():
    # Get the filename from the query parameter
    filename = request.args.get('file')
    
    if not filename:
        return abort(400, description="No file specified.")
    
    # Secure the filename to prevent directory traversal
    filename = secure_filename(filename)
    
    # Check if the file is allowed
    if not allowed_file(filename):
        return abort(400, description="Invalid file type.")
    
    # Construct the full file path
    file_path = os.path.join(IMAGE_BASE_PATH, filename)
    
    # Check if the file exists and is a file (not a directory)
    if not os.path.isfile(file_path):
        return abort(404, description="File not found.")
    
    # Serve the file with the lowest necessary privileges
    # Ensure that the web server is configured to run with limited privileges
    return send_file(file_path)

if __name__ == '__main__':
    app.run()

