from flask import Flask, request, redirect, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change to a strong secret key
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# Assuming a User model with username and password_hash fields
class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(80), primary_key=True)
    password_hash = db.Column(db.String(120))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Fetch user from the database
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password is correct
        if user and bcrypt.check_password_hash(user.password_hash, password):
            session['username'] = user.username  # Create a session for the user
            return redirect('/home')
        else:
            return redirect('/login')
    else:
        # If the user is already logged in, redirect to home
        if 'username' in session:
            return redirect('/home')
        return open('login.html').read()

@app.route('/home')
def home():
    # Ensure the user is authenticated before accessing the home page
    if 'username' not in session:
        return redirect('/login')
    return 'Welcome to the home page!'

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the user session
    return redirect('/login')

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use SSL/TLS for secure HTTP communication

