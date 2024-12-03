from flask import Flask, request, redirect, session, render_template, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import os

app = Flask(__name__)

# Load secret key from environment variable or fail if not set
app.secret_key = os.environ.get('SECRET_KEY')
if not app.secret_key:
    raise RuntimeError("SECRET_KEY is not set in the environment variables.")

# Configure database (use environment variables for production)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Enable CSRF protection
csrf = CSRFProtect(app)

# Define User model with hashed passwords
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Increased hash length

# Ensure session cookies are secure
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Session timeout set to 1 hour

# Define login required decorator
def ensure_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kws)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session.modified = True  # Ensure the session is marked as modified
            return redirect('/secret')
        else:
            return jsonify({'error': 'Invalid login credentials'}), 401
    return render_template('login.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings')
@ensure_logged_in
def settings():
    # Settings page logic here
    return 'Confidential settings page'

@app.route('/secret')
@ensure_logged_in
def secret():
    # Secret page logic here
    return 'Confidential secret page'

@app.route('/logout', methods=['POST'])
@csrf.exempt
def logout():
    session.pop('user_id', None)
    return redirect('/')

# Additional security headers including CSP
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    # Add other headers as needed
    return response

if __name__ == '__main__':
    # Ensure database exists
    db.create_all()

    # Run the app with SSL context only in development
    # In production, use a proper SSL/TLS setup
    app.run(ssl_context='adhoc' if os.environ.get('FLASK_ENV') == 'development' else None)

