import os
from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import mimetypes

# Initialize the Flask application
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = '/path/to/uploads'  # Outside of the web document root
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}  # Allowed file types
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB upload limit

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    # Check if the file has an allowed extension (case-insensitive)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Secure the filename before storing it
            filename = secure_filename(file.filename)
            # Disallow path elements in uploaded file names
            if '/' in filename or '\\' in filename:
                flash('Invalid file path')
                return redirect(request.url)
            # Save the file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File uploaded successfully'
        else:
            flash('File type not allowed')
            return redirect(request.url)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run()

