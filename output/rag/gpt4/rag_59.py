from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a real secret key
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Encrypt the username before querying the database
        encrypted_username = bcrypt.hashpw(username.encode('utf-8'), bcrypt.gensalt())

        # Query the database safely with parameterized SQL
        user = User.query.filter_by(username=encrypted_username).first()

        if user and user.check_password(password):
            # Redirect to home page if the password is correct
            return redirect(url_for('home'))
        else:
            # Flash a message and return to the login page if the password is incorrect
            flash('Invalid username or password')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/home')
def home():
    # Home page code goes here
    return 'Welcome to the home page!'

if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)

