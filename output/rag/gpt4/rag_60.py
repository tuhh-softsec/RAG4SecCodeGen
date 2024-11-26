from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Verify the origin page of the request
        if 'Referer' not in request.headers or not request.headers['Referer'].endswith('/login'):
            return redirect('/internal_server_error')

        username = request.form['username']
        password = request.form['password']

        try:
            user = User.query.filter_by(username=username).first()
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                # Redirect to success page if authentication is successful
                return redirect('/success')
            else:
                # Redirect to login failure page if authentication fails
                return redirect('/cant_login')
        except SQLAlchemyError:
            # Redirect to internal server error page if there is a database error
            return redirect('/internal_server_error')
    else:
        # Apply authentication before returning the requested page
        # This could be a check for a session cookie or token
        # For simplicity, we'll just render the login page here
        return render_template('login.html')

@app.route('/success')
def success():
    # Secure content that requires authentication
    return 'Login successful!'

@app.route('/cant_login')
def cant_login():
    # Inform the user that login was unsuccessful
    return 'Unable to login. Please check your username and password.'

@app.route('/internal_server_error')
def internal_server_error():
    # Inform the user that an internal server error occurred
    return 'An internal server error occurred. Please try again later.', 500

if __name__ == '__main__':
    app.run(debug=True)

