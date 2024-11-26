from flask import Flask, render_template, request, make_response, session
import os
import html

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key for session management

# Decorator to require authentication
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'authenticated' not in session:
            # Redirect to login page or return an error
            return "Access denied. Please log in.", 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/hello/<username>')
@login_required
def hello(username):
    # Encode the username to prevent XSS attacks
    safe_username = html.escape(username)

    # Render the template with the safe username
    return render_template('hello.html', username=safe_username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Perform authentication (e.g., check username and password)
        # This is a placeholder for actual authentication logic
        username = request.form['username']
        password = request.form['password']
        if authenticate(username, password):
            session['authenticated'] = True
            # Generate a pseudorandom value for the session cookie
            session['csrf_token'] = os.urandom(16).hex()
            response = make_response("Logged in successfully.")
            return response
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

def authenticate(username, password):
    # Placeholder function for authenticating a user
    # In a real application, you would check the credentials against a user database
    return username == "admin" and password == "password"

if __name__ == '__main__':
    app.run()

