from flask import Flask, request, abort, session, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_session import Session
import os
import hmac
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Configure Flask session with secure options
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

# Load or generate a persistent secret key
SECRET_KEY_FILE = 'secret.key'
if os.path.exists(SECRET_KEY_FILE):
    with open(SECRET_KEY_FILE, 'rb') as f:
        app.config['SECRET_KEY'] = f.read()
else:
    app.config['SECRET_KEY'] = os.urandom(24)
    with open(SECRET_KEY_FILE, 'wb') as f:
        f.write(app.config['SECRET_KEY'])

Session(app)

# Configure application to not run in debug mode in production
app.config['DEBUG'] = False

# Set up logging
handler = RotatingFileHandler('admin_access.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# Function to simulate fetching hashed password from a secure store
def get_admin_credentials():
    # Fetch credentials from a secure environment variable or secret management tool
    admin_password_hash = os.environ.get('ADMIN_PASSWORD_HASH')
    if not admin_password_hash:
        raise ValueError("Admin password hash not found in environment variables")
    return 'admin', admin_password_hash

# Function to check if the provided password matches the stored hash
def check_password(password_hash, password):
    return bcrypt.check_password_hash(password_hash, password)

@app.route('/admin/login', methods=['POST'])
def admin_access():
    '''
    Read the username and password from the request,
    validate the username and password for admin access,
    and create a secure session for the admin user.
    '''
    # Extract username and password from request
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        abort(400, 'Missing username or password')

    # Fetch the stored hashed password for the admin user
    admin_username, admin_password_hash = get_admin_credentials()

    # Check if the provided username matches the admin username using constant-time comparison
    if hmac.compare_digest(username, admin_username):
        # Compare the provided password with the stored hash
        if check_password(admin_password_hash, password):
            session['admin_logged_in'] = True
            app.logger.info('Admin login successful')
            return redirect(url_for('admin_dashboard'))
        else:
            app.logger.warning('Admin login failed: Invalid password')
            abort(401, 'Invalid credentials')
    else:
        app.logger.warning('Admin login failed: Invalid username')
        abort(401, 'Invalid credentials')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return 'Admin Dashboard'

# Run the Flask app with SSL in production
if __name__ == '__main__':
    context = ('path/to/ssl/cert.pem', 'path/to/ssl/key.pem')  # Replace with your actual SSL certificate and key files
    try:
        app.run(ssl_context=context)
    except Exception as e:
        app.logger.error(f'Failed to start with SSL context: {e}')

