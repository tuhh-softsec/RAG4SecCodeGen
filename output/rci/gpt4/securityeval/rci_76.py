import bcrypt
import os
from flask import Flask, request, session, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import logging
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin.db'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(minutes=20)

db = SQLAlchemy(app)

# Configure rate limiting to prevent brute force attacks
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)

# Configure logging to avoid recording sensitive information
logging.basicConfig(filename='admin_access.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/admin/login', methods=['POST'])
@limiter.limit("5 per minute")  # Apply rate limiting to the login route
def admin_access():
    '''
    Authenticate the admin user and set the session state.
    '''
    # Extract username and password from the request
    username = request.form.get('username')
    password = request.form.get('password')

    # Input validation (more robust validation)
    if not username or not password or len(username) > 50 or len(password) > 50:
        return jsonify({"error": "Invalid input"}), 400

    try:
        # Retrieve the hashed password from the database
        user = User.query.filter_by(username=username).first()
    except SQLAlchemyError as e:
        logging.error(f'Database error: {e}')
        return jsonify({"error": "Service unavailable"}), 503

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        session.regenerate()  # Regenerate session ID to prevent fixation
        session['admin_logged_in'] = True  # Set the session state
        logging.info(f'Admin {username} logged in successfully.')
        return jsonify({"message": "Access granted"}), 200
    else:
        logging.warning(f'Invalid login attempt for username: {username}.')
        return jsonify({"error": "Invalid username or password"}), 401

@app.before_first_request
def create_tables():
    db.create_all()

@app.before_first_request
def set_security_headers():
    # Set security headers
    Flask.response_class.default_headers['X-Content-Type-Options'] = 'nosniff'
    Flask.response_class.default_headers['X-Frame-Options'] = 'SAMEORIGIN'
    Flask.response_class.default_headers['Content-Security-Policy'] = "default-src 'self'"

if __name__ == '__main__':
    # Load SSL/TLS certificate and private key for production use
    context = ('path/to/cert.pem', 'path/to/key.pem')
    app.run(ssl_context=context)

# Example usage:
# Send a POST request to /admin/login with 'username' and 'password' form fields

