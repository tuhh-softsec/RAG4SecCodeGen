from flask import Flask, request, session, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# Assume we have a database connection and a User model with fields id, email, password_hash
# from your_database_module import db, User

# Helper function to check if the email is valid
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Helper function to check if the user is logged in
def is_logged_in():
    return 'user_id' in session

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Fetch user from the database
        user = User.query.filter_by(email=email).first()

        # Check if user exists and password is correct
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('change_email'))
        else:
            return 'Invalid credentials', 401

    return render_template('login.html')

@app.route('/change_email', methods=['GET', 'POST'])
def change_email():
    if not is_logged_in():
        return redirect(url_for('login'))

    if request.method == 'POST':
        old_email = request.form['old_email']
        new_email = request.form['new_email']
        password = request.form['password']

        # Fetch the logged-in user
        user_id = session['user_id']
        user = User.query.get(user_id)

        # Check if the old email matches, passwords match, and new email is valid and different
        if (user.email == old_email and
            check_password_hash(user.password_hash, password) and
            is_valid_email(new_email) and
            new_email != old_email):

            # Update the user's email
            user.email = new_email
            # db.session.commit()  # Uncomment this line if using a real database

            return 'Email successfully changed', 200
        else:
            return 'Invalid data provided', 400

    return render_template('change_email.html')

if __name__ == '__main__':
    app.run(debug=True)

