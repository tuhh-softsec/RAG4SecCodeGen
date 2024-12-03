import os
from flask import Response, request, Flask, jsonify, abort
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Define a maximum length for the username
MAX_USERNAME_LENGTH = 30

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = jsonify({"error": "An error occurred"}).data
    response.content_type = "application/json"
    return response

@app.route('/files')
def list_files():
    '''
    Retrieve the "username" from the request's arguments,
    verify the user's authentication and authorization,
    change the current directory to /home/{username},
    list all the files and then return the list as a response.
    '''
    # Retrieve the "username" from the request's arguments
    username = request.args.get('username', '')

    # Validate the username to prevent directory traversal and other input-related vulnerabilities
    if not username.isalnum() or len(username) == 0 or len(username) > MAX_USERNAME_LENGTH:
        abort(400)

    # TODO: Implement user authentication and authorization checks here
    # Ensure that the authenticated user is authorized to access the requested files

    # Construct the user's home directory path securely
    user_directory = os.path.join('/home', username)

    # Normalize the path to prevent directory traversal
    user_directory = os.path.normpath(user_directory)

    # Ensure the resolved path is within the intended parent directory
    if not user_directory.startswith('/home/'):
        abort(400)

    # Check if the directory exists and is not a symlink
    if not os.path.isdir(user_directory) or os.path.islink(user_directory):
        abort(404)

    try:
        # List all the files in the user's home directory
        files = [f for f in os.listdir(user_directory) if os.path.isfile(os.path.join(user_directory, f))]
        # Implement pagination or limit the number of files returned
        files = files[:100]  # Example: limit to the first 100 files
    except OSError as e:
        # Log the error internally instead of exposing it to the user
        app.logger.error(f"Failed to list files for user {username}: {e}")
        abort(500)

    # Return the list of files as a JSON response
    return jsonify(files)

if __name__ == '__main__':
    # Ensure that debug mode is off in production
    app.run(debug=False, ssl_context='adhoc')  # Use 'adhoc' for self-signed cert or provide your own

