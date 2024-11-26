from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from os import urandom

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = urandom(24)
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

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

        # Guideline #4: Compare the hash of an incoming password to a saved hash
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect('/dashboard')
        else:
            return redirect('/login')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Guideline #2: Apply authentication before returning the requested page
    if 'user_id' not in session:
        return redirect('/login')

    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

@app.route('/first-login', methods=['GET', 'POST'])
def first_login():
    # Guideline #1: "First login" mode
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username)
        user.set_password(password)  # Set a unique strong password
        db.session.add(user)
        db.session.commit()
        return redirect('/login')

    return render_template('first_login.html')

if __name__ == '__main__':
    app.run(debug=True)

