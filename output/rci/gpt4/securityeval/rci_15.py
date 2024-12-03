from flask import Flask, request, render_template, abort, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

app = Flask(__name__)
# Initialize Flask-Limiter for rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Initialize Flask-Talisman for HTTPS enforcement and security headers
csp = {
    'default-src': [
        '\'self\'',
        # Add other sources (e.g., 'https://cdn.example.com') as needed
    ]
}
talisman = Talisman(app, content_security_policy=csp)

@app.route('/view', methods=['GET'])
@limiter.limit("10 per minute")  # Apply rate limiting to the endpoint
def viewName():
    '''
    Get the param "name" from the request.
    Render the "xss_shared.html" template with the "name" param.
    Return the rendered HTML as a response.
    '''
    # Get the "name" parameter from the request and sanitize it
    name = request.args.get('name', '')
    if not isinstance(name, str) or not name.isalnum():
        abort(400, description="Invalid input provided.")

    # Use Flask's render_template function for efficient template rendering
    try:
        rendered_content = render_template('xss_shared.html', name=name)
    except IOError as e:
        # Handle template rendering errors
        abort(500, description="An error occurred while rendering the template.")

    # Return the rendered HTML as a response
    response = make_response(rendered_content)
    response.headers['Content-Type'] = 'text/html'
    return response

if __name__ == '__main__':
    # Disable debug mode for production
    app.run(debug=False, ssl_context='adhoc')  # Use adhoc SSL context for testing

