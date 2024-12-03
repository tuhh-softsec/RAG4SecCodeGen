import os
from canvasapi import Canvas
from flask import Flask, request, session, abort, jsonify
from urllib.parse import urlparse
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config['DEBUG'] = False  # Turn off debugging in production
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookie
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')  # Set a secret key for session signing

# Load Canvas API URL and access token from environment variables
API_URL = os.environ.get('CANVAS_API_URL')
API_KEY = os.environ.get('CANVAS_API_KEY')

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

# Set up rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = jsonify({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.route('/get_assignments/<int:course_id>')
@limiter.limit("10 per minute")  # Adjust the rate limit as appropriate
def get_assignments(course_id):
    if not session.get('logged_in'):
        abort(401)  # Unauthorized access

    if not user_has_permission(course_id):
        abort(403)  # Forbidden access

    parsed_url = urlparse(request.base_url)
    if not is_valid_host(parsed_url.hostname):
        abort(400)  # Bad Request

    try:
        course = canvas.get_course(course_id)
        assignments = course.get_assignments()

        # Only expose necessary assignment properties
        assignments_list = [{
            'id': assignment.id,
            'name': assignment.name,
            'description': assignment.description,
            'due_at': assignment.due_at
        } for assignment in assignments]

        return jsonify({'assignments': assignments_list})
    except canvasapi.exceptions.CanvasException as e:
        # Log the exception for debugging purposes
        app.logger.error(f'Error fetching assignments: {e}')
        abort(500)  # Internal Server Error

def user_has_permission(course_id):
    # Implement your logic to check if the user has the right to access the course
    # Example: Check if the course_id is in the list of courses the user is allowed to access
    user_courses = get_user_courses()  # You need to implement this function
    return course_id in user_courses

def is_valid_host(hostname):
    # Implement your logic to validate the hostname
    # Example: Check if the hostname matches your application's domain
    return hostname in ['yourappdomain.com', 'sub.yourappdomain.com']

def get_user_courses():
    # Implement your logic to retrieve a list of course IDs the user has access to
    # This could involve checking user roles, permissions, and database records
    return [123, 456, 789]  # Replace with actual logic

if __name__ == '__main__':
    # Use a production-ready WSGI server like Gunicorn instead of app.run()
    # Example: gunicorn -w 4 'myapp:create_app()'
    pass

