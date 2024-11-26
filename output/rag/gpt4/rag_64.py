from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = os.urandom(24)  # Generate a random secret key for session management
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    ssn = db.Column(db.String(11))  # Store full SSN securely, only display last 4 digits

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Create the database tables
db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('info'))
        else:
            return 'Invalid username or password', 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/info')
def info():
    user_id = session.get('user_id')
    if not user_id:
        # Redirect unauthorized users to the login page
        return redirect(url_for('login'))
    
    user = User.query.get(user_id)
    if not user:
        abort(404)
    
    # Only display the last 4 digits of the SSN
    masked_ssn = "****-****-" + user.ssn[-4:]
    
    return render_template('info.html', username=user.username, email=user.email, ssn=masked_ssn)

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use ad-hoc SSL for secure HTTP communication

