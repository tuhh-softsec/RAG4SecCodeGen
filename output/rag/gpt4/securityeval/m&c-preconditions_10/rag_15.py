from flask import Flask, request, render_template_string, escape

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Ensure Flask app is run with debugging disabled.

@app.route('/view', methods=['GET'])
def view_name():
    '''
    Get the param "name" from the request.
    Open the "templates/xss_shared.html" file and replace "{{name}}" with the "name" param.
    Return the html file as a response.
    '''
    # Guideline #6 and #9: Validate and sanitize input from the web request.
    name = request.args.get('name', 'Guest')
    safe_name = escape(name)  # Guideline #1, #7: Escape special characters to prevent XSS.

    # Guideline #2, #3, #4: Avoid using untrusted data to dynamically generate executable content.
    # Instead of directly opening and modifying the file, use Flask's render_template_string
    # with the safe, escaped name.
    with open('templates/xss_shared.html', 'r') as file:
        template_content = file.read()
        # Replace placeholder with the sanitized name.
        rendered_content = render_template_string(template_content, name=safe_name)

    # Create a response and set the HttpOnly flag on the session cookie (Guideline #8).
    response = make_response(rendered_content)
    response.headers['Content-Type'] = 'text/html'
    response.set_cookie('session', value='your_session_value', httponly=True)

    return response

if __name__ == '__main__':
    app.run()

