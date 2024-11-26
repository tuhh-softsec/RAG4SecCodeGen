from flask import Flask, session, redirect, url_for, request, render_template
from functools import wraps

app = Flask(__name__)

# Set the secret key to a complex random value for secure sessions
app.secret_key = 'your_complex_random_secret_key_here'

# Decorator to check if the user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'authenticated' not in session or not session['authenticated']:
            # Redirect to login page if the user is not authenticated
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Authenticate the user (this is a placeholder for actual authentication logic)
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            session['authenticated'] = True
            session['username'] = username
            # Store sensitive information securely in the session
            session['email'] = get_user_email(username)
            session['ssn_last_4'] = get_user_ssn_last_4(username)
            # Set the session cookie to HttpOnly
            session.modified = True
            response = app.make_response(redirect(url_for('info')))
            response.headers['Set-Cookie'] = 'session={}; HttpOnly'.format(session.sid)
            return response
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/info')
@login_required
def info():
    # Ensure that the session contains the required information
    if 'username' in session and 'email' in session and 'ssn_last_4' in session:
        # Render a template with the user's information
        return render_template('info.html', username=session['username'], email=session['email'], ssn_last_4=session['ssn_last_4'])
    else:
        # If the session does not contain the required information, redirect to login
        return redirect(url_for('login'))

def authenticate_user(username, password):
    # Placeholder function for authenticating a user
    # Replace with actual authentication logic
    return True

def get_user_email(username):
    # Placeholder function to get user's email
    # Replace with actual logic to retrieve user's email from the database
    return 'user@example.com'

def get_user_ssn_last_4(username):
    # Placeholder function to get user's SSN last 4 digits
    # Replace with actual logic to retrieve user's SSN from the database
    return '1234'

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use SSL/TLS to encrypt the traffic

