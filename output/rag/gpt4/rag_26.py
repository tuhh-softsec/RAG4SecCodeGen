import os
from flask import Flask, request, send_from_directory, abort

app = Flask(__name__)

SAFE_DIRECTORY = '/safe/'

def is_safe_path(basedir, path, follow_symlinks=True):
    # Check if the path is safe to access
    if follow_symlinks:
        return os.path.realpath(path).startswith(basedir)
    return os.path.abspath(path).startswith(basedir)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # Ensure that the filename does not contain path elements to satisfy Guideline #5
    if '/' in filename or '\\' in filename:
        abort(400, "Invalid filename")

    # Construct the full file path
    file_path = os.path.join(SAFE_DIRECTORY, filename)

    # Check if the path is safe to access
    if not is_safe_path(SAFE_DIRECTORY, file_path):
        abort(403, "Access denied")

    # Serve the file
    try:
        return send_from_directory(SAFE_DIRECTORY, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404, "File not found")

if __name__ == '__main__':
    # Run the app in a secure environment
    app.run(secure=True)

