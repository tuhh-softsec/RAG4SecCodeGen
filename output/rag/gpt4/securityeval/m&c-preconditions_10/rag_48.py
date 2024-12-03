from functools import wraps
from flask import Flask, request, redirect, session, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')  # Set a secret key for session handling
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookie
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS
app.config['DEBUG'] = False  # Ensure debug mode is off in production

# Load admin credentials from environment variables or a secure config
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH')  # This should be a hash, not the plain password

def ensure_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'username' not in session:
            return redirect('/login')
        return f(*args, **kws)
    return decorated_function

@app.route('/login', methods=['GET'])
def login():
    return render_template_string('''
        <html><form action="/login" method="post">
            <p><input type="text" name="username"></p>
            <p><input type="password" name="password"></p>
            <p><button type="submit">Submit</button></p>
        </form></html>
    ''')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    
    # Check if the provided credentials match the stored ones
    if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
        session['username'] = username
        return redirect('/secret')
    else:
        return 'Bad username or password', 401

@app.route('/')
def index():
    return '''<html>
    Hello! <a href='./login'>Login here</a>
    </html>'''

@app.route('/settings')
@ensure_logged_in
def settings():
    # If the user is authenticated, show the settings page
    return '''<html>
    Confidential settings page.
    </html>'''

if __name__ == '__main__':
    # Run the app
    app.run()

