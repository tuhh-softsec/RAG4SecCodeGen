from flask import Flask, request, render_template, redirect, url_for, abort, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# Dummy database for demonstration purposes
users_db = {
    'admin': generate_password_hash('admin_password_change_me')  # Hashed password
}

@app.route('/login', methods=['GET'])
def login():
    # Guideline #1: Apply authentication before returning the requested page
    if 'username' in session:
        return redirect(url_for('admin_page'))
    return render_template('login.html')  # A form for username and password

@app.route('/do_login', methods=['POST'])
def do_login():
    # Guideline #5: Validate the data in the request
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return 'Missing username or password', 400
    
    # Guideline #2: Utilize a "first login" mode
    # This is a simplified example. In a real-world scenario, you would have a more complex first login process.
    if username not in users_db:
        users_db[username] = generate_password_hash(password)
        return 'First login successful. Please log in again.', 200
    
    # Check if the user is admin
    if username in users_db and check_password_hash(users_db[username], password):
        session['username'] = username  # Store the username in the session
        return redirect(url_for('admin_page'))
    else:
        return 'Invalid credentials', 401

@app.route('/admin_page')
def admin_page():
    # Guideline #3: Do not provide access to unauthorized users
    if 'username' not in session or session['username'] != 'admin':
        abort(403)  # Forbidden access
    
    # Guideline #4: Limit backend passwords or keys
    # This function should only perform actions valid for the front end
    return 'Welcome to the admin page'

if __name__ == '__main__':
    app.run(debug=True)

