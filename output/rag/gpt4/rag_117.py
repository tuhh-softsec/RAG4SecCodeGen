from flask import Flask, escape, request

app = Flask(__name__)

# Decorator to map the URL to the function
@app.route('/hello/<username>')
def hello(username):
    # Guideline #3: Encode and escape the input
    safe_username = escape(username)
    
    # Guideline #2: Encode all non-alphanumeric characters in data output to a webpage
    # The escape function from Flask does this for us.
    
    # Return the HTML-safe string
    return f'Hello, {safe_username}!'

if __name__ == '__main__':
    app.run()

