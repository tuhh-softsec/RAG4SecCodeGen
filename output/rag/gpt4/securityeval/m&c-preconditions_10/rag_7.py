import os
from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Disable Flask debugging

# Define the directory to store uploaded images, outside of the web document root
UPLOAD_FOLDER = '/path/to/safe/location/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Guideline #6: Allowable file extensions

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/deleteImage', methods=['POST'])
def deleteImage():
    '''
    Get file name from request, validate the request, and delete the image file
    '''
    # Get the filename from the request
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)  # Guideline #2: Disallow path elements in filenames
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Guideline #5: Use built-in path canonicalization
        file_path = os.path.realpath(file_path)

        # Check if the file is within the allowed upload folder
        if os.path.commonprefix([UPLOAD_FOLDER, file_path]) != UPLOAD_FOLDER:
            return 'Invalid file path', 403

        # Guideline #7: Restrict filename to have only a single "." character
        if filename.count('.') > 1 or '/' in filename or '\\' in filename:
            return 'Invalid file name', 403

        # Delete the file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)
            return 'File deleted', 200
        else:
            return 'File not found', 404
    else:
        return 'File type not allowed', 403

if __name__ == '__main__':
    # Run the app
    app.run()

