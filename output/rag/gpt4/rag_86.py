import os
from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import subprocess
import shlex

UPLOAD_FOLDER = '/path/to/uploads'  # Outside of the web document root
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super_secret_key'  # Change this to a random secret key

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
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            flash('File successfully uploaded')
            # Execute the file in a sandboxed environment (if needed)
            # execute_in_sandbox(file_path)
            return redirect(url_for('upload_file'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def execute_in_sandbox(file_path):
    # This function should execute the file in a sandboxed environment
    # such as a chroot jail or a Docker container with limited privileges.
    # This is a placeholder for the sandbox execution logic.
    # Ensure that the file is not malicious and is safe to execute.
    pass

if __name__ == '__main__':
    app.run(debug=True)

