from flask import Flask, request, redirect, render_template, make_response, session
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key for the session

# Function to insert user message into the database
def insert_user_message_in_db(username, message):
    # Implementation of the function that securely inserts the message into the database
    pass

@app.route('/post', methods=['POST'])
def post_message():
    try:
        username = request.form['username']
        message = request.form['message']
        
        # Input validation to prevent XSS and SQL injection
        if not username.isalnum() or not message:
            raise ValueError("Invalid input")
        
        # Insert the message into the database
        insert_user_message_in_db(username, message)
        
        # Redirect to the home page
        return redirect('/')
    except Exception as e:
        # Log the detailed error message with restricted access
        app.logger.error(f"Error posting message: {e}")
        
        # Display a generic error message to the user
        return "An error occurred. Please try again later.", 500

@app.route('/')
def index():
    # Retrieve messages from the database (implementation not shown)
    messages = get_messages_from_db()
    
    # Render the messages in the template, ensuring that they are properly escaped to prevent XSS
    return render_template('index.html', messages=messages)

# Function to retrieve messages from the database
def get_messages_from_db():
    # Implementation of the function that securely retrieves messages from the database
    pass

# Set a secure cookie with a pseudorandom value
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)
    if 'csrf_token' not in session:
        session['csrf_token'] = os.urandom(16).hex()

if __name__ == '__main__':
    app.run()

