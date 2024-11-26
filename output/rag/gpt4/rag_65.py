from flask import Flask, session, request, redirect, url_for, abort, make_response
from functools import wraps

app = Flask(__name__)

# Set the secret key to a random bytes, this should be kept secret
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Helper function to check if a user is authenticated
def is_authenticated():
    return 'authenticated' in session and session['authenticated']

# Decorator to protect a route with authentication
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            # Redirect to login page or return 401 Unauthorized
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Login route to authenticate user and set session variables
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Here you would verify username and password from the form
        # For simplicity, we'll assume the user is authenticated
        session['authenticated'] = True
        session['username'] = 'user123'
        session['email'] = 'user123@example.com'
        session['ssn'] = '123-45-6789'
        # Set the session cookie to HttpOnly
        session_cookie = request.cookies.get(app.session_cookie_name)
        response = make_response(redirect(url_for('info')))
        response.set_cookie(app.session_cookie_name, session_cookie, httponly=True)
        return response
    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

# Route to display user information
@app.route('/info')
@login_required
def info():
    # Ensure that the user has an active and authenticated session
    if not is_authenticated():
        abort(401)  # Unauthorized access

    # Retrieve user information from the session
    username = session.get('username')
    email = session.get('email')
    ssn = session.get('ssn')

    # Return the user information as a string
    return f'Username: {username}, Email: {email}, SSN: {ssn}'

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use SSL/TLS to encrypt the traffic

