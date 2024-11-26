from flask import Flask, request, make_response, session, escape
import subprocess
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)  # Generate a secure secret key for the session

# Decorator to bind a function to a URL
@app.route('/ping', methods=['POST'])
def ping():
    # Security Guideline #1: Set a pseudorandom value as a cookie
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_urlsafe(16)
    response = make_response()

    # Retrieve the URL to ping from the session state (Security Guideline #2)
    url = session.get('url_to_ping')
    if not url:
        return "No URL provided in the session", 400

    # Security Guideline #3, #4, #5: Ensure that the URL is properly escaped to prevent XSS
    safe_url = escape(url)

    # Execute the ping command securely (Security Guideline #2)
    try:
        # Use subprocess to run the ping command with shell=False to prevent command injection
        result = subprocess.run(['ping', '-c', '1', safe_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        pong = result.stdout.decode('utf-8') + result.stderr.decode('utf-8')

        # Check the return code to determine if the URL is alive
        if result.returncode == 0:
            response.data = f"URL {safe_url} is alive.\n{pong}"
        else:
            response.data = f"URL {safe_url} is not alive.\n{pong}"
    except Exception as e:
        response.data = f"An error occurred: {str(e)}"

    return response

# Route to set the URL to ping in the session
@app.route('/set_url', methods=['POST'])
def set_url():
    url = request.form.get('url')
    if url:
        # Store the URL in the session state (Security Guideline #2)
        session['url_to_ping'] = url
        return "URL set successfully", 200
    else:
        return "No URL provided", 400

if __name__ == '__main__':
    app.run(debug=True)

