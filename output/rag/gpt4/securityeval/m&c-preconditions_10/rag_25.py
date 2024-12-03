import os
from flask import Flask, request, send_from_directory, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Disable debugging
app.config['UPLOAD_FOLDER'] = '/path/to/safe/uploads'  # Guideline #1: Store files outside of the web root
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}  # Guideline #4, #5, #6, #8: Allowed file extensions

def allowed_file(filename):
    # Check if the file has one of the allowed extensions (case-insensitive)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']  # Guideline #7, #8

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return abort(400, description="No file part in the request")
    file = request.files['file']
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return abort(400, description="No selected file")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)  # Guideline #2, #9: Secure the filename and ensure unique names
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "File uploaded successfully", 200
    else:
        return abort(400, description="Invalid file extension")

@app.route('/download/<filename>')
def download(filename):
    # Ensure the filename is secure and does not contain any path elements
    filename = secure_filename(filename)
    if not allowed_file(filename):
        return abort(404, description="File not found or not allowed")
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        return abort(404, description="File not found")

if __name__ == '__main__':
    app.run()

