from flask import Flask, send_from_directory, abort, request
import os
import re

app = Flask(__name__)

# Define the base directory for images, outside of the web document root
IMAGE_DIR = '/path/to/secure/image/storage'

# A decorator to associate the URL of /img with the img() function
@app.route('/img/<name>')
def img(name):
    # Security Guideline #2: Avoid server-side script injection
    # Sanitize the 'name' parameter to prevent directory traversal attacks
    # and ensure it only contains valid characters for a filename
    sanitized_name = re.sub(r'[^a-zA-Z0-9_.-]', '', name)

    # Security Guideline #4: Perform case-insensitive evaluations of the extension
    # Check if the file extension is allowed (e.g., .jpg, .png, .gif)
    if not re.match(r'^.*\.(jpg|jpeg|png|gif)$', sanitized_name, re.IGNORECASE):
        abort(404)  # If the extension is not allowed, return a 404 error

    # Construct the full file path
    file_path = os.path.join(IMAGE_DIR, sanitized_name)

    # Security Guideline #1: Store uploaded files outside of the web document root
    # Check if the file exists and is within the IMAGE_DIR to prevent directory traversal
    if not os.path.isfile(file_path) or not os.path.realpath(file_path).startswith(IMAGE_DIR):
        abort(404)  # If the file does not exist or is outside IMAGE_DIR, return a 404 error

    # Send the file from the secure directory
    return send_from_directory(IMAGE_DIR, sanitized_name)

# Additional code to handle file uploads securely
@app.route('/upload', methods=['POST'])
def upload_file():
    # Security Guideline #3: Assign unique names to uploaded files
    # Security Guideline #5: Store utility files outside of the web document root
    # (Implementation of file upload handling goes here, with unique naming and secure storage)

    # Placeholder response for this example
    return "File uploaded successfully", 200

if __name__ == '__main__':
    app.run()

