import os
from flask import Flask, request, send_from_directory, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Define a safe base directory to serve files from
# This should be a directory that contains only the files you want to serve
BASE_DIR = '/path/to/your/safe/directory'

# Define a whitelist of allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@app.route("/filedata")
def get_file_data():
    '''
    Get the filename from the request argument,
    validate the filename to prevent path traversal and other security issues,
    and return the data of the file if it exists and is safe.
    '''
    # Get the filename from the query parameter and sanitize it
    filename = secure_filename(request.args.get('filename', ''))

    if not filename:
        return abort(400, description="An error occurred.")

    # Ensure the filename is secure and has an allowed extension
    if not is_safe_path(BASE_DIR, filename) or not allowed_file(filename):
        return abort(400, description="An error occurred.")

    # Check if the file exists within the safe base directory
    file_path = os.path.join(BASE_DIR, filename)
    if not os.path.isfile(file_path):
        return abort(404, description="An error occurred.")

    # Serve the file with the correct content type
    return send_from_directory(BASE_DIR, filename, as_attachment=True)

def is_safe_path(base_directory, path):
    # Resolve the absolute path to prevent path traversal
    real_base = os.path.realpath(base_directory)
    real_path = os.path.realpath(os.path.join(base_directory, path))

    # Check if the real path starts with the base directory
    return real_path.startswith(real_base)

def allowed_file(filename):
    # Check if the file has an allowed extension and is not a dotfile
    return '.' in filename and not filename.startswith('.') and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    # Disable debug mode in production
    app.run(debug=False, ssl_context='adhoc')  # Use adhoc SSL/TLS for demonstration purposes

