from flask import Flask, request, redirect, make_response, render_template, session
import os
import secrets

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for sessions

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_urlsafe(64)
    return session['_csrf_token']

@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

@app.route('/post', methods=['POST'])
def post():
    username = request.form['username']
    message = request.form['message']
    
    # Insert the message into the database
    insert_user_message_in_db(username, message)
    
    # Redirect the user back to the main page
    return redirect('/')

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        return post()
    else:
        # Render the main page with the CSRF token
        return render_template('main_page.html', csrf_token=generate_csrf_token())

def insert_user_message_in_db(username, message):
    # Insert the user's message into the database securely
    # This is a placeholder function. Implement the actual database logic here.
    pass

if __name__ == '__main__':
    app.run()

