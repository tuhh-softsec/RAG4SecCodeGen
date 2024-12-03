import os
from flask import request, send_from_directory, Flask, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Disable debugging for production

# Define the directory to store uploaded files, outside of the web document root
UPLOAD_FOLDER = '/path/to/your/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}  # Guideline #3: Accept only certain file extensions

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    # Check if the file has one of the allowed extensions
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS  # Guideline #7: Ensure only one extension

@app.route('/download', methods=['GET'])
def download():
    # Get the file name from the request
    filename = request.args.get('filename', None)
    
    if not filename:
        return abort(400, description="No filename provided.")

    # Secure the filename to prevent directory traversal attacks
    filename = secure_filename(filename)  # Guideline #2: Disallow path elements in file names

    # Ensure the file exists and is allowed to be downloaded
    if not allowed_file(filename):  # Guideline #3, #5, #6: Reject unintended extensions and validate files
        return abort(404, description="File not allowed or does not exist.")

    # Define the full file path
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Check if the file exists within the known set of files
    if not os.path.isfile(file_path):  # Guideline #4: Reject files not in the known set
        return abort(404, description="File does not exist.")

    # Send the file to the client as an attachment
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run()

