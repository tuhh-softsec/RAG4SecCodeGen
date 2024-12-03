from flask import Flask, request, redirect, abort
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10
app.config['UPLOAD_FOLDER'] = '/path/to/uploads'  # Guideline #1: Outside of web root
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}  # Guideline #7, #8, #9

def allowed_file(filename):
    # Check if the file has one of the allowed extensions (case-insensitive)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']  # Guideline #8, #9

@app.route('/pdf/upload', methods=['POST'])
def upload_pdf():
    # Check if the post request has the file part
    if 'file' not in request.files:
        abort(400, 'No file part in the request')
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        abort(400, 'No selected file')
    if file and allowed_file(file.filename):  # Guideline #7, #8, #9
        filename = secure_filename(file.filename)  # Guideline #2
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/pdf/view')
    else:
        abort(400, 'Invalid file type or extension')

# This route is just a placeholder and should be implemented properly
@app.route('/pdf/view')
def view_pdf():
    return 'PDF view page (not implemented)'

if __name__ == '__main__':
    app.run()

