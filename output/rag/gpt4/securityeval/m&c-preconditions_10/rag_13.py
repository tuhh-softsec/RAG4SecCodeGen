from flask import Flask, request, render_template_string, abort
from jinja2 import Environment, FileSystemLoader, select_autoescape
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Ensure Flask app is run with debugging disabled.

# Guideline #5: Prevent users from making further requests if their limit has been exceeded.
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Guideline #1: Avoid setting Jinja2 autoescape to False.
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

@app.route('/render')
@limiter.limit("10 per minute")  # Apply rate limit to this endpoint.
def render_response_from_env():
    '''
    Get the argument "name" from request, 
    create a jinja2 Environment,
    get the template.html from the environment, and render it.
    '''
    # Guideline #7: Do not accept untrusted data as input from a web request.
    name = request.args.get('name', 'Guest')
    
    # Guideline #2, #3, #4, #8: Appropriately encode all non-alphanumeric characters in data.
    # Jinja2 autoescape is enabled, so it will automatically escape variables rendered in the template.
    
    # Guideline #6: Ensure the requesting user is authorized to access a protected object.
    # This example does not include user authentication, but in a real application,
    # you would check user permissions here before proceeding.
    
    # Load the template and render it with the provided name.
    try:
        template = env.get_template('template.html')
    except TemplateNotFound:
        abort(404)  # Template not found, return 404 error.

    # Render the template with the sanitized 'name' variable.
    rendered_template = template.render(name=name)
    
    return render_template_string(rendered_template)

if __name__ == '__main__':
    app.run()

