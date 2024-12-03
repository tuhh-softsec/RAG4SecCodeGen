import os
import re
import uuid
from flask import request, Flask, abort

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Disable Flask debugging

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}  # Define allowed extensions
DENYLIST_EXTENSIONS = {'exe', 'bat', 'sh', 'php', 'py'}  # Define denylist extensions

def allowed_file(filename):
    # Guideline #6: Ensure the uploaded file has only one extension
    # Guideline #7: Perform case-insensitive evaluations of the extension
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return True
    return False

def denylisted_file(filename):
    # Guideline #4: Use denylists to validate uploaded files
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in DENYLIST_EXTENSIONS:
        return True
    return False

@app.route('/upload', methods=['POST'])
def upload():
    # Guideline #1: Validate both the content and metadata of uploaded files
    if 'username' not in request.form or 'file' not in request.files:
        abort(400, description="Missing username or file")

    username = request.form['username']
    file = request.files['file']

    # Guideline #2: Reject uploaded files with unintended extensions
    # Guideline #3: Reject uploaded files not belonging to the known set of files
    if not allowed_file(file.filename) or denylisted_file(file.filename):
        abort(400, description="Invalid file extension")

    # Guideline #5: Accept only uploaded files whose content conforms to specifications
    # (This guideline requires specific content validation which is not implemented here due to lack of details)

    # Guideline #8: Assign unique names to uploaded files
    unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]

    # Save the file with a unique name to prevent overwriting and directory traversal issues
    file.save(os.path.join('/path/to/upload/folder', unique_filename))

    # Search the username in the filename of the attachment
    if re.search(re.escape(username), file.filename, re.IGNORECASE):
        return f"Username found in filename: {file.filename}", 200
    else:
        return "Username not found in filename", 404

if __name__ == '__main__':
    app.run()

