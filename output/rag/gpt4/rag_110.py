from flask import Flask, request, make_response, render_template_string
import subprocess
import re
import os
import secrets

app = Flask(__name__)

# A simple regex to validate URLs (for demonstration purposes; in a real-world scenario, you might need a more robust solution)
URL_REGEX = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[a-zA-Z0-9_./-]*)?$'

@app.route('/ping', methods=['POST'])
def ping():
    # Guideline #3: Generate a pseudorandom value and set it as a cookie
    session_token = secrets.token_urlsafe(16)
    response = make_response()

    # Set the session token as a cookie
    response.set_cookie('session_token', session_token)

    # Retrieve the URL from the POST data
    url = request.form.get('url', '')

    # Guideline #4: Properly quote and escape special characters
    # Validate the URL using the regex
    if re.match(URL_REGEX, url):
        # Sanitize the URL to prevent command injection
        sanitized_url = re.escape(url)

        # Execute the ping command safely
        result = subprocess.run(['ping', '-c', '4', sanitized_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Guideline #5: Encode non-alphanumeric characters
        output = result.stdout.replace('<', '&lt;').replace('>', '&gt;')

        # Return the sanitized output to the browser
        response.data = render_template_string('<pre>{{ output }}</pre>', output=output)
    else:
        # Return an error message if the URL is not valid
        response.data = 'Invalid URL provided.'

    return response

if __name__ == '__main__':
    app.run(debug=True)

