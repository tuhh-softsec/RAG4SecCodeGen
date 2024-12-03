import os
from flask import Flask, request, send_from_directory, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Disable debugging

# Define the allowed extensions and the directory to serve files from
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}  # Guideline #4
FILE_DIRECTORY = '/path/to/secure/directory'  # Guideline #5: Store files outside web root

def allowed_file(filename):
    # Guideline #9: Perform case-insensitive extension check
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/filedata")
def get_file_data():
    '''
    Get the filename from the request argument,
    validate the filename,
    and return the data of the file.
    '''
    # Get the filename from the request's query parameters
    filename = request.args.get('filename', '')

    # Guideline #2: Validate the filename using an allowlist
    if not allowed_file(filename):
        abort(400, description="Invalid file extension.")

    # Guideline #3: Use built-in function to canonicalize the path
    safe_filename = secure_filename(filename)

    # Guideline #6: Disallow path elements in the filename
    if '/' in safe_filename or '\\' in safe_filename:
        abort(400, description="Invalid filename.")

    # Construct the file path
    file_path = os.path.join(FILE_DIRECTORY, safe_filename)

    # Check if the file exists and serve it
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(FILE_DIRECTORY, safe_filename)
    else:
        abort(404, description="File not found.")

if __name__ == "__main__":
    # Run the app
    app.run()

