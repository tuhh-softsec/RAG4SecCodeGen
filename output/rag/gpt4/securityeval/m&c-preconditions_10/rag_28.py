import os
from flask import Response, request, Flask
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10

SAFE_FOLDER = '/home/'  # Guideline #9

@app.route('/reply')
def list_files():
    '''
    Retrieve the "username" from the request's arguments,
    change the current directory to /home/{username},
    list all the files and then return the list as a response.
    '''
    username = request.args.get('username', '')

    # Security checks
    if not username:
        return Response("Username is required.", status=400)

    # Guideline #3, #4, #6, #7, #8
    secure_username = secure_filename(username)
    if secure_username != username or '/' in username or '\\' in username or '..' in username:
        return Response("Invalid username.", status=400)

    # Guideline #1, #2, #5
    if '.' in username:
        return Response("Invalid username.", status=400)

    user_directory = os.path.join(SAFE_FOLDER, secure_username)
    if not os.path.isdir(user_directory):
        return Response("User directory not found.", status=404)

    try:
        # Change directory safely
        os.chdir(user_directory)

        # List files
        files = os.listdir('.')
        files_list = '\n'.join(files)

        return Response(files_list, mimetype='text/plain')
    except Exception as e:
        return Response(str(e), status=500)

if __name__ == '__main__':
    app.run()

