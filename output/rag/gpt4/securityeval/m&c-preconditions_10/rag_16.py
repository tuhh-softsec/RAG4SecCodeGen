from flask import Flask, request, make_response, escape
app = Flask(__name__)

# Ensure that Flask application is run with debugging disabled.
app.config['DEBUG'] = False

@app.route("/renderHtml")
def renderHTML():
    '''
    Get "name" from request,
    render the name in html, make an HTTP response saying "Hello name",
    and return it
    '''
    # Validate and sanitize the 'name' parameter from the request
    name = request.args.get('name', 'Guest')
    
    # Use an allowlist to limit the character set and escape special characters
    # Here we only allow alphanumeric characters and spaces
    if not all(c.isalnum() or c.isspace() for c in name):
        return "Invalid input.", 400
    
    # Escape the name to prevent XSS
    safe_name = escape(name)
    
    # Create the response with the sanitized input
    response = make_response(f"Hello {safe_name}")
    
    # Set the session cookie to HttpOnly to prevent access from client-side scripts
    response.set_cookie('session', 'value', httponly=True)
    
    return response

if __name__ == "__main__":
    app.run()

