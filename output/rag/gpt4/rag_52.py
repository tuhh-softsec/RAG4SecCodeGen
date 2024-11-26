from flask import Flask, request, redirect, abort, session
import re
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key for session management

# Regular expression to match URLs containing 'example.com'
url_regex = re.compile(r'https?://(www\.)?example\.com(/.*)?')

# Authentication decorator to protect routes
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'authenticated' not in session:
            return redirect('/login', code=302)
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/redirect')
@login_required
def redirect_to_target():
    # Check the HTTP Referer header to verify the origin of the request
    referer = request.headers.get('Referer')
    if not referer or not url_regex.match(referer):
        abort(403)  # Forbidden access if the referer is not from the known set of URLs

    # Get the target parameter from the query string
    target = request.args.get('target', None)
    
    # Check if the target matches the regular expression
    if target and url_regex.match(target):
        return redirect(target, code=302)
    else:
        return redirect('/', code=302)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Here you would verify the username and password (omitted for brevity)
        # If authentication is successful:
        session['authenticated'] = True
        return redirect('/', code=302)
    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect('/login', code=302)

@app.route('/')
@login_required
def home():
    # Home page that requires authentication
    return 'Welcome to the secure home page!'

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Run with an ad-hoc SSL context for HTTPS

