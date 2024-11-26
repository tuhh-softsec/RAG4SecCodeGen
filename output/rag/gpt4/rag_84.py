import os
import base64
import imghdr
import uuid
from flask import request, abort

# Define the path to store uploaded files outside of the web document root
UPLOAD_FOLDER = '/path/to/secure/storage'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image_stream(stream):
    header = stream.read(512)  # Read the first 512 bytes to check the file type
    stream.seek(0)  # Reset the stream position
    file_format = imghdr.what(None, header)
    if not file_format:
        return False
    return file_format.lower() in ALLOWED_EXTENSIONS

def upload_image():
    # Check if the post request has the file part
    if 'file' not in request.files:
        abort(400, 'No file part')

    file = request.files['file']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        abort(400, 'No selected file')

    if file and allowed_file(file.filename):
        # Validate the content of the image
        if not validate_image_stream(file.stream):
            abort(400, 'Invalid image content')

        # Generate a unique name for the image using UUID
        unique_filename = str(uuid.uuid4())
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{unique_filename}.{file_extension}"

        # Read the image and encode it using base64
        encoded_image = base64.b64encode(file.read())

        # Write the encoded image to a file
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, 'wb') as f:
            f.write(encoded_image)

        return f"Image successfully uploaded and stored as {filename}"
    else:
        abort(400, 'Unsupported file type')

# Ensure the UPLOAD_FOLDER exists and is writable
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

