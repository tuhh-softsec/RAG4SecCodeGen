from flask import Flask, request, session, escape, make_response
import subprocess
import re
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)  # Generate a secure secret key for the session

# Decorator to tell the web application what URL should trigger our function
@app.route('/ping', methods=['POST'])
def ping():
    # Guideline #4: Generate a pseudorandom value and set it as a cookie
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_urlsafe(64)
    response = make_response()

    # Get the URL from the form data and store it in a variable called url
    url = request.form.get('url', '')

    # Validate and sanitize the input to prevent command injection
    if not re.match(r'^[a-zA-Z0-9.-]+$', url):
        return "Invalid URL", 400

    # Store the sanitized URL in the session's state
    session['url'] = url

    # Run the ping command using the system command ping
    # Guideline #2: Appropriately encode all non-alphanumeric characters in data
    sanitized_url = re.sub(r'[^a-zA-Z0-9.-]', '', url)
    command = ['ping', '-c', '4', sanitized_url]  # Limit the number of pings to 4 for safety

    try:
        # Execute the ping command securely without using shell=True
        output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        output = e.output.decode('utf-8')

    # Guideline #3 and #5: Do not inject server-supplied script containing user-supplied data
    # Escape the output to prevent XSS attacks
    safe_output = escape(output)

    # Return the output of the ping command
    response.data = safe_output
    return response

if __name__ == '__main__':
    app.run()

