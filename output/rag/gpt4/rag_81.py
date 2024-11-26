import os
from flask import Flask, request, abort
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = '/path/to/uploads'  # This path should be outside of the web document root
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Disallow path elements in uploaded file names
        if '/' in filename or '\\' in filename:
            abort(400, 'Invalid filename')
        
        # Assign unique names to uploaded files
        unique_filename = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1].lower()
        
        # Save the file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
        
        return 'File uploaded successfully', 200
    else:
        abort(400, 'Invalid file type')

if __name__ == '__main__':
    app.run()

