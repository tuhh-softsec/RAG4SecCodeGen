import os
from flask import Flask, request, jsonify, abort, Response
from flask_limiter import Limiter
from flask_limiter.util import get_ipaddr
from werkzeug.utils import secure_filename
from functools import wraps
import jwt
import re

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # Limit file size to 1MB
app.config['UPLOAD_FOLDER'] = '/path/to/your/images/directory'
app.config['DEBUG'] = False  # Ensure debug mode is off in production
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with your secret key
app.config['JWT_ALGORITHM'] = 'HS256'  # Replace with your preferred algorithm

# Set up rate limiting
limiter = Limiter(
    app,
    key_func=get_ipaddr,  # Adjusted to get the real IP address if behind a proxy
    default_limits=["5 per minute"]
)

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            abort(401, description="Missing Authorization header.")
        
        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[app.config['JWT_ALGORITHM']])
        except jwt.ExpiredSignatureError:
            abort(401, description="Token expired.")
        except (jwt.InvalidTokenError, IndexError):
            abort(401, description="Invalid token.")
        
        if not user_is_authorized(payload):
            abort(403, description="User not authorized.")
        
        return f(*args, **kwargs)
    return decorated_function

# Helper function to check if a user is authorized
def user_is_authorized(payload):
    # Implement your authorization logic here
    # For example, check if the token payload has the right permissions
    return payload.get('is_admin', False)

@app.route('/deleteImage/<filename>', methods=['DELETE'])
@require_auth
@limiter.limit("1 per second")  # Rate limit to prevent abuse
def deleteImage(filename):
    '''
    Delete the image file with the given filename
    '''
    # Validate filename against a whitelist of allowed characters
    if not re.match(r'^[\w,\s-]+\.[A-Za-z]{3}$', filename):
        abort(400, description="Invalid filename.")
    
    # Sanitize the filename to avoid directory traversal
    filename = secure_filename(filename)

    # Construct the full file path
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found."}), 404

    # Delete the file
    try:
        # Implement file-locking mechanism here if necessary
        os.remove(file_path)
        # Confirm file deletion
        if os.path.exists(file_path):
            raise Exception("File deletion failed.")
        return jsonify({"success": True}), 200
    except Exception as e:
        # Log the error without sensitive information
        app.logger.error(f"Error deleting a file: {str(e)}")
        return jsonify({"error": "An error occurred while deleting the file."}), 500

if __name__ == '__main__':
    # Enforce HTTPS in production by setting up SSL context or using a reverse proxy
    app.run(ssl_context='adhoc')  # Example of running with an ad-hoc SSL context

