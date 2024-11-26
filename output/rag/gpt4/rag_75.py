from flask import Flask, request, redirect, url_for, render_template, session, abort
from functools import wraps
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key for session management

# Helper function to check if a user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Helper function to check if a user is an admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session or not session['admin']:
            abort(403)  # Forbidden access
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/do_login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Here you would validate the username and hashed_password against your user store
    # For this example, we'll assume any non-empty username and password is valid
    if username and password:
        session['logged_in'] = True
        session['username'] = username
        session['admin'] = username == 'admin'  # Simple check to assign admin role
        return redirect(url_for('index'))
    else:
        return 'Invalid credentials', 401

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/user_page')
@login_required
def user_page():
    return render_template('user_page.html', username=session['username'])

@app.route('/admin_page')
@login_required
@admin_required
def admin_page():
    return render_template('admin_page.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

