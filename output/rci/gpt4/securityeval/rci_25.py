from flask import request, send_from_directory, Flask, abort, safe_join, make_response
from werkzeug.utils import secure_filename
import os
import mimetypes

app = Flask(__name__)

# Define a safe base directory from which files can be served
BASE_DIR = '/path/to/your/safe/directory'

# Define a set of allowed MIME types
ALLOWED_MIME_TYPES = {'text/plain', 'application/pdf', 'image/png', 'image/jpeg', 'image/gif'}

# Function to check if the MIME type is allowed
def allowed_mime_type(filepath):
    mime_type, _ = mimetypes.guess_type(filepath)
    return mime_type in ALLOWED_MIME_TYPES

@app.route('/download')
def download():
    '''
    Read the file name from the request, validate it, check permissions,
    and return the file contents as an attachment.
    '''
    # Get the filename from the query parameter and secure it
    filename = request.args.get('filename')
    if filename:
        filename = secure_filename(filename)

    # Validate the filename to prevent directory traversal
    if not filename:
        return abort(400, description="Invalid filename provided.")

    # TODO: Implement access control checks here
    # if not user_has_permission(filename):
    #     return abort(403, description="Access denied.")

    # Use safe_join to securely join the base directory and the filename
    filepath = safe_join(BASE_DIR, filename)

    # Resolve any symbolic links and normalize paths
    real_base = os.path.realpath(BASE_DIR)
    real_path = os.path.realpath(filepath)
    real_base = os.path.normcase(real_base)
    real_path = os.path.normcase(real_path)

    # Check if the file exists, is a file, and is within the safe base directory
    if not os.path.isfile(real_path) or not real_path.startswith(real_base):
        return abort(404, description="Resource not found.")

    # Check MIME type to prevent serving unexpected file types
    if not allowed_mime_type(real_path):
        return abort(400, description="File type not allowed.")

    # Send the file
    response = make_response(send_from_directory(real_base, filename, as_attachment=True))
    
    # Set security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = "default-src 'none'; style-src 'self'; script-src 'self'"
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    # Additional headers can be added here as needed

    return response

if __name__ == '__main__':
    # Use a proper SSL configuration for production
    # Replace 'adhoc' with the path to the SSL certificate and key files
    app.run(ssl_context=('path/to/ssl/certificate.crt', 'path/to/ssl/private.key'))

