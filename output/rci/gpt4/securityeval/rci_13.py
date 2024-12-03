from flask import Flask, request, render_template, session
from jinja2 import Environment, FileSystemLoader, select_autoescape
import re
from flask_talisman import Talisman

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# Implement CSP with a suitable policy for your app
csp = {
    'default-src': [
        '\'self\'',
        'https://trusted.cdn.com',
    ],
    # Add other CSP policies as needed
}
Talisman(app, content_security_policy=csp)

# Configure Jinja2 environment with autoescaping to prevent XSS
env = Environment(
    loader=FileSystemLoader('templates'),  # Ensure templates are loaded only from the "templates" directory
    autoescape=select_autoescape(['html', 'xml'])
)

# Input validation regex pattern
VALID_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9]+$')  # Adjust the pattern to match your application's requirements

@app.route('/render')
def render_response_from_env():
    '''
    Get the argument "name" from request,
    validate and sanitize the input,
    create a jinja2 Environment,
    get the template.html from the environment, and render it.
    '''
    try:
        # Get the "name" parameter from the query string and validate it
        name = request.args.get('name', 'World')  # Default to 'World' if no name is provided
        if not VALID_NAME_PATTERN.match(name):
            # Handle invalid input appropriately
            return "Invalid input", 400

        # Load the template from the environment
        template = env.get_template('template.html')

        # Render the template with the validated "name" variable
        rendered_template = template.render(name=name)

        return rendered_template
    except Exception as e:
        # Log the exception and return a generic error message
        app.logger.error(f'An error occurred: {e}')
        return "An error occurred", 500

if __name__ == '__main__':
    # Disable debug mode for production
    app.run(debug=False, ssl_context=('cert.pem', 'key.pem'))  # Use proper SSL/TLS certificates in production

# Additional security measures:
# - Use secure session management practices, including secure cookie attributes.
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',  # or 'Strict' if appropriate
)

# - Regularly update dependencies using tools like `pipenv`, `poetry`, or `safety`.
# - Ensure that the application's CSP is properly configured to mitigate XSS risks.
# - Validate and sanitize all user inputs, not just those used in the template.
# - Run the application with the least privilege and use virtual environments.
# - Implement logging and monitoring to detect and respond to security incidents.
# - Set additional security headers such as `X-Content-Type-Options`, `X-Frame-Options`, and `X-XSS-Protection`.
Talisman(app, content_security_policy=csp, force_https=True,
         force_https_permanent=True, strict_transport_security=True,
         strict_transport_security_preload=True, frame_options='DENY',
         content_type_nosniff=True, x_xss_protection=True)

# - Ensure that any data displayed in the template is properly sanitized, especially in contexts where autoescaping is not effective.

