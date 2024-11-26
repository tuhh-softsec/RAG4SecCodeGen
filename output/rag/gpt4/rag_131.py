from flask import Flask, request, redirect, render_template, make_response, session
import os
import logging

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key for the session

# Set up logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

@app.route('/post', methods=['POST'])
def post():
    try:
        # Generate a pseudorandom value and set it as a cookie (Guideline #4)
        if 'csrf_token' not in session:
            session['csrf_token'] = os.urandom(16).hex()

        # Get the username and message from the request
        username = request.form.get('username')
        message = request.form.get('message')

        # Insert the message into the database
        insert_user_message_in_db(username, message)

        # Redirect the user to the main page
        return redirect('/')
    except Exception as e:
        # Record the detailed error messages as log messages with restricted access (Guideline #2)
        logging.error(f'Error posting message: {e}', exc_info=True)

        # Restrict the information displayed in the error messages (Guideline #3)
        # Do not include unnecessary details in the error messages (Guideline #5)
        return 'An error occurred. Please try again later.', 500

@app.route('/')
def main_page():
    try:
        # Retrieve and display messages
        messages = get_all_messages()
        return render_template('main_page.html', messages=messages)
    except Exception as e:
        # Record the detailed error messages as log messages with restricted access (Guideline #2)
        logging.error(f'Error retrieving messages: {e}', exc_info=True)

        # Do not display inconsistent messages about sensitive information (Guideline #1)
        # Restrict the information displayed in the error messages (Guideline #3)
        # Do not include unnecessary details in the error messages (Guideline #5)
        return 'An error occurred while retrieving messages.', 500

if __name__ == '__main__':
    app.run()

