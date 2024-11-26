import os
import base64
import imghdr
from werkzeug.utils import secure_filename
from flask import request
from sqlalchemy import create_engine

# Configure your database connection here
DATABASE_URI = 'sqlite:///your_database.db'
engine = create_engine(DATABASE_URI)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return 'No selected file', 400

    if file and allowed_file(file.filename):
        # Secure the filename to avoid directory traversal attacks
        filename = secure_filename(file.filename)

        # Generate a unique name for the image to avoid filename collisions
        unique_filename = str(uuid.uuid4()) + os.path.splitext(filename)[1]

        # Read the image and convert to base64
        image_data = file.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        # Verify the image type
        image_type = imghdr.what(None, h=image_data)
        if not image_type or image_type not in ALLOWED_EXTENSIONS:
            return 'Invalid image type', 400

        # Insert the image name and base64 string into the database
        try:
            with engine.connect() as connection:
                connection.execute(
                    "INSERT INTO images (name, data) VALUES (%s, %s)",
                    (unique_filename, image_base64)
                )
        except Exception as e:
            # Handle database errors
            return str(e), 500

        return 'Image successfully uploaded', 200
    else:
        return 'File type not allowed', 400

