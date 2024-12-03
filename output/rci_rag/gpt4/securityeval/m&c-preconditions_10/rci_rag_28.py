import os
from flask import Flask, jsonify, request, abort, session
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, login_required, current_user
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_talisman import Talisman

app = Flask(__name__)
app.config['DEBUG'] = False  # Ensure debug mode is off
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a real secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Configure your database URI
app.config['SESSION_TYPE'] = 'filesystem'  # Configure session type

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
Session(app)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["5 per minute"])
Talisman(app)  # Enable HTTPS and set security headers

# Set up logging
logging.basicConfig(filename='access.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Define the User model (simplified for example purposes)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Other fields like password_hash would be here

    def check_password(self, password):
        # Placeholder for password checking logic
        return True

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        return jsonify({"message": "Logged in successfully"}), 200
    return abort(401)

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/files')
@login_required
@limiter.limit("5 per minute")  # Apply rate limiting
def list_files():
    '''
    List all the files in the authenticated user's directory and return the list as a response.
    '''
    # Get the authenticated user from the current_user proxy
    user = current_user

    # Construct the safe file path
    base_directory = app.config.get('BASE_DIRECTORY', '/home')
    user_directory = os.path.join(base_directory, secure_filename(user.username))
    real_user_directory = os.path.realpath(user_directory)

    # Ensure the path is within the base directory
    if not real_user_directory.startswith(os.path.realpath(base_directory)):
        abort(403)

    try:
        # List all files in the user's directory
        files = os.listdir(real_user_directory)
    except OSError as e:
        # Log the error
        logging.error(f"Error listing files for user {user.username}: {e}")
        abort(500)

    # Log the successful access
    logging.info(f"User {user.username} listed files in their directory")

    # Return the list of files as a response
    return jsonify(files)

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use ad-hoc SSL for demonstration purposes

