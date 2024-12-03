import os
from flask import Flask, request, send_from_directory, abort, jsonify
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from logging.handlers import RotatingFileHandler
from flask_talisman import Talisman

app = Flask(__name__)
app.config['DEBUG'] = False  # Disable Flask debugging

# Define the allowed extensions and the directory to serve files from
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
FILES_DIRECTORY = '/path/to/secure/directory'

# Set up rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Set up logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# Set up security headers with Talisman
talisman = Talisman(app)

def allowed_file(filename):
    # Check if the file has an allowed extension
    ext = os.path.splitext(filename)[1].lower()
    if ext.startswith('.'):
        ext = ext[1:]
    return ext in ALLOWED_EXTENSIONS

@app.route("/filedata", methods=['GET'])
@limiter.limit("10 per minute")  # Apply rate limiting to the endpoint
def getFileData():
    '''
    Get the filename from the request argument,
    validate the filename,
    and return the data of the file.
    '''
    # Get the filename from the request's query parameters
    filename = request.args.get('filename', '')

    # Sanitize and validate the filename
    if not filename:
        abort(400, description="No filename provided.")
    filename = secure_filename(filename)
    if not allowed_file(filename):
        abort(400, description="File extension not allowed.")

    # Prevent directory traversal
    real_path = os.path.realpath(os.path.join(FILES_DIRECTORY, filename))
    if not real_path.startswith(os.path.realpath(FILES_DIRECTORY)):
        abort(400, description="Invalid file path.")

    # Serve the file if it exists
    try:
        response = send_from_directory(FILES_DIRECTORY, filename, as_attachment=True)
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        return response
    except FileNotFoundError:
        abort(404, description="File not found.")
    except Exception as e:
        app.logger.error(f'Unhandled exception: {e}')
        abort(500, description="An error occurred while processing your request.")

if __name__ == "__main__":
    # Run the app with a production WSGI server like Gunicorn, not with app.run()
    pass

