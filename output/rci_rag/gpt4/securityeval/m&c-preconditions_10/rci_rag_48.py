from flask import Flask, request, redirect, session, render_template, abort, flash
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Load secret key from environment variable and fail if not set
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
if not app.config['SECRET_KEY']:
    raise ValueError("The FLASK_SECRET_KEY environment variable must be set to a secure value.")

app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent client-side scripts from accessing the session cookie
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Mitigate CSRF attacks by restricting how cookies are sent with cross-site requests

# CSRF protection
csrf = CSRFProtect(app)

# Dummy database for demonstration purposes
# In a real application, use a proper database and store hashed passwords
users_db = {
    'admin': generate_password_hash('unique_strong_password')
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists and the password is correct
        if username in users_db and check_password_hash(users_db[username], password):
            session.regenerate()  # Rotate session identifier after login
            session['username'] = username
            return redirect('/settings')
        else:
            flash('Invalid login credentials.')  # Use a generic error message
            return redirect('/login')
    return render_template('login.html')

@app.route('/settings')
def settings():
    if 'username' not in session:
        return redirect('/login')
    # If the user is authenticated, show the settings page
    return render_template('settings.html', username=session['username'])

# Ensure that the application is not accessible if run directly
if __name__ == "__main__":
    print("This script is not meant to be run directly.")
    import sys
    sys.exit(1)

