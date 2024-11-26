from flask import Flask, request, session, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# Assuming a function to get user data from the database
def get_user_by_email(email):
    # This function should retrieve the user record from the database by email
    pass

# Assuming a function to update user email in the database
def update_user_email(user_id, new_email):
    # This function should update the user's email in the database
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = get_user_by_email(email)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            return redirect(url_for('change_email'))
        else:
            flash('Invalid email or password')
    
    return render_template('login.html')

@app.route('/change-email', methods=['GET', 'POST'])
def change_email():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        old_email = request.form['old_email']
        new_email = request.form['new_email']
        confirm_password = request.form['confirm_password']
        
        user = get_user_by_email(old_email)
        
        if user and session['user_id'] == user['id']:
            if check_password_hash(user['password_hash'], confirm_password):
                if re.match(r"[^@]+@[^@]+\.[^@]+", new_email):  # Simple email validation
                    update_user_email(user['id'], new_email)
                    flash('Email successfully changed')
                else:
                    flash('Invalid new email format')
            else:
                flash('Incorrect password')
        else:
            flash('Invalid request')
    
    return render_template('change_email.html')

if __name__ == '__main__':
    app.run(debug=True)

