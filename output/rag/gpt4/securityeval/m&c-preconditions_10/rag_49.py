import secrets
from flask import Flask, request, render_template, make_response, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Replace with your actual database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = False  # Ensure debugging is disabled

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Ensure you create the database and add users with hashed passwords before running the app
# db.create_all()

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session_id = secrets.token_hex(16)
        response = make_response(redirect(url_for('index')))
        response.set_cookie('session_id', session_id, httponly=True, secure=True, samesite='Lax')
        # Store the session ID securely in your database or server-side session
        # e.g., session_store[session_id] = user.id
        return response
    else:
        return 'Invalid credentials', 401

@app.route('/')
def index():
    # Your main page logic here
    return 'Welcome to the secure app!'

if __name__ == '__main__':
    app.run()

