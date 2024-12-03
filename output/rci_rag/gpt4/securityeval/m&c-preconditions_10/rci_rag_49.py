import os
from flask import Flask, request, render_template, redirect, url_for, session, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

# Import a secure configuration from an external file
import config

app = Flask(__name__)
app.config.from_object(config)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize Flask-Session for server-side session management
Session(app)

# Initialize rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1 per second"]  # More strict rate limiting
)

# Dummy function to simulate checking credentials against a secure data store
def check_credentials(username, password):
    # In a real application, you would fetch the user's hashed password
    # from a database and use check_password_hash to compare it.
    # For demonstration purposes, we're using a hardcoded hash.
    user_password_hash = generate_password_hash('secure_password')
    return check_password_hash(user_password_hash, password)

@app.route('/login', methods=['GET', 'POST'])
@csrf.exempt  # Exempt this route from CSRF token requirement
@limiter.limit("1 per second")  # Apply rate limiting to login attempts
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check whether the credentials are valid
        if check_credentials(username, password):
            # Clear the session before setting new values to prevent session fixation
            session.clear()

            # Set the user_id in the session
            session['user_id'] = username  # Use a unique identifier for the user

            return redirect(url_for('index'))
        else:
            abort(401)  # Use abort to handle incorrect login attempts
    return render_template('login.html')

@app.route('/')
def index():
    # Display the main page of the application
    return 'Welcome to the secure app!'

if __name__ == '__main__':
    # Ensure that Flask application is run with debugging disabled
    app.run(debug=False, ssl_context=('path/to/cert.pem', 'path/to/key.pem'))  # Use proper SSL/TLS context

