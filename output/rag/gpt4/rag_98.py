from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Generate a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Database URI
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# Create the database tables
db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Encrypt the username and password information
        # For demonstration purposes, we're only hashing the password.
        # In a real-world scenario, you might use a separate encryption method for the username.
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))

        # Create a new user with the hashed password
        new_user = User(username=username, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch the user by username
        user = User.query.filter_by(username=username).first()

        # Compare the hash of the incoming password to the saved hash
        if user and bcrypt.check_password_hash(user.password_hash, password):
            flash('Login successful!', 'success')
            # Redirect to a secure page (not implemented in this example)
            return redirect(url_for('secure_page'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/secure_page')
def secure_page():
    # Placeholder for a secure page after successful login
    return 'Welcome to the secure page!'

if __name__ == '__main__':
    app.run(debug=True)

