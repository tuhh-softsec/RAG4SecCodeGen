from flask import Flask, request, render_template, abort, session, make_response
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2.exceptions import TemplateNotFound
import os
import re
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from flask_talisman import Talisman

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Set a random secret key
app.config['DEBUG'] = False  # Disable debug mode
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Secure session cookies
app.config['SESSION_COOKIE_SECURE'] = True  # Transmit cookies over HTTPS only
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Restrict cookies to same site requests
app.config['SESSION_COOKIE_DOMAIN'] = '.example.com'  # Set the domain for the session cookie
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Set session expiration time (in seconds)

# Initialize the rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Talisman for security headers
talisman = Talisman(app, content_security_policy=None)

# Define a list of allowed template names
ALLOWED_TEMPLATES = {'template.html'}

# Define a regex pattern for allowed characters in filenames
ALLOWED_FILENAME_CHARS = re.compile(r'^[\w\-. ]+$')

# Define a function to sanitize and validate the template name
def sanitize_template_name(template_name):
    sanitized_name = os.path.basename(template_name)
    if sanitized_name in ALLOWED_TEMPLATES and ALLOWED_FILENAME_CHARS.match(sanitized_name):
        return sanitized_name
    return None

@app.route('/render')
@limiter.limit("10 per minute")  # Apply rate limiting to the endpoint
def render_response_from_env():
    template_name = request.args.get('name', 'template.html')
    sanitized_template_name = sanitize_template_name(template_name)
    if not sanitized_template_name:
        abort(400, description="Invalid template name.")
    
    env = Environment(
        autoescape=select_autoescape(['html', 'xml']),
        loader=FileSystemLoader('templates')
    )
    
    try:
        template = env.get_template(sanitized_template_name)
    except TemplateNotFound:
        abort(404, description="Template not found.")
    
    # Render the template with user-supplied data, ensuring it is properly escaped
    user_data = session.get('user_data', {})
    # Validate and sanitize user_data before rendering
    # (Assuming a sanitize_user_data function exists)
    sanitized_user_data = sanitize_user_data(user_data)
    rendered_template = template.render(user_data=sanitized_user_data)
    
    response = make_response(rendered_template)
    # Set additional security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response

if __name__ == '__main__':
    # Use a production-ready SSL context instead of 'adhoc'
    app.run(ssl_context=('cert.pem', 'key.pem'))  # Replace with paths to your actual certificate and key files

