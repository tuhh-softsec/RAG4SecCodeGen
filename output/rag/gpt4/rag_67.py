from flask import Flask, request, send_from_directory, abort
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Define the path to the images folder, which should be outside of the web document root
IMAGES_FOLDER = '/path/to/secure/images/folder'

# Decorator to specify the URL that triggers the function
@app.route('/images/<filename>')
def get_image(filename):
    # Guideline #1: Verify the origin page of the request
    if 'Referer' not in request.headers:
        abort(403)  # Forbidden access if no Referer header is present

    # Guideline #5: Prevent the submission of modified filepaths
    # Use secure_filename to ensure that the filename is safe
    filename = secure_filename(filename)

    # Check if the file exists in the images folder
    file_path = os.path.join(IMAGES_FOLDER, filename)
    if os.path.isfile(file_path):
        # Send the file to the browser
        return send_from_directory(IMAGES_FOLDER, filename)
    else:
        # If the file does not exist, return a 404 Not Found response
        abort(404)

if __name__ == '__main__':
    app.run()

