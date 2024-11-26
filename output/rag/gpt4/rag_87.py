import os
import uuid
import imghdr
from werkzeug.utils import secure_filename
from flask import Flask, request, abort

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists and is not within the web document root
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def verify_image_type(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        abort(400, 'No file part')

    file = request.files['file']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        abort(400, 'No selected file')

    if file and allowed_file(file.filename):
        # Disallow path elements in uploaded file names
        filename = secure_filename(file.filename)

        # Assign a unique name to the uploaded file
        unique_filename = str(uuid.uuid4()) + verify_image_type(file.stream)
        if unique_filename is None:
            abort(400, 'Invalid image type')

        # Save the file to the uploads folder
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)

        # If you need to execute the file, create an isolated account with limited privileges
        # and use it to execute the file in a sandboxed environment. This is highly context-specific
        # and requires careful consideration of security implications.

        return 'File uploaded successfully', 200

    else:
        abort(400, 'File type not allowed')

if __name__ == '__main__':
    app.run()

