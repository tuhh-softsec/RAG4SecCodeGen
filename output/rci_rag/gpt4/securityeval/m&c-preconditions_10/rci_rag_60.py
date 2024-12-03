import os
from flask import Flask, session, redirect, url_for, request
from flask_session import Session
from datetime import timedelta

app = Flask(__name__)

# Load the secret key from an environment variable or configuration file
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')

# Flask application configuration for security
app.config['DEBUG'] = False  # Disable debugging in production
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent client-side scripts from accessing the session cookie
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)  # Set session lifetime (e.g., 1 hour)

# Initialize server-side session management
app.config['SESSION_TYPE'] = 'filesystem'  # Use server-side sessions
Session(app)

# Function to set security headers on responses
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains'
    return response

# Example login route that regenerates the session ID upon authentication
@app.route('/login', methods=['POST'])
def login():
    # Authenticate the user here
    user_authenticated = True  # Replace with actual authentication logic
    if user_authenticated:
        session.regenerate()  # Regenerate the session ID to prevent session fixation
        session['user_id'] = 'user_id_here'  # Store the authenticated user's ID in the session
        return redirect(url_for('index'))
    return 'Invalid credentials', 401

# Function to invalidate the session
@app.route('/logout')
def logout():
    session.clear()  # Clear the entire session
    response = redirect(url_for('index'))
    response = set_security_headers(response)  # Set security headers on the response
    return response

# Apply security headers to all responses
@app.after_request
def apply_security_headers(response):
    return set_security_headers(response)

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use ad-hoc SSL/TLS for demonstration purposes

