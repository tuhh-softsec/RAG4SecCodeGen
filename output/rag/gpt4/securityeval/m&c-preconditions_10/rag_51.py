from flask import Flask, request, session, redirect, url_for
from canvasapi import Canvas
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a real secret key
app.config['SESSION_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['DEBUG'] = False  # Ensure debug mode is off in production

# Assuming you have a function to check user authentication
def is_authenticated():
    return 'user_id' in session

# Assuming you have a function to get the API URL and key securely
def get_canvas_api_credentials():
    # Retrieve securely stored API credentials
    # For example, from environment variables, a secure key store, etc.
    api_url = 'your_canvas_instance_api_url'
    api_key = 'your_securely_stored_api_key'
    return api_url, api_key

@app.route('/course/<int:course_id>/assignments')
def get_assignments(course_id):
    if not is_authenticated():
        # Redirect to login page if the user is not authenticated
        return redirect(url_for('login'))

    # Get the API credentials securely
    api_url, api_key = get_canvas_api_credentials()

    # Initialize a new Canvas object
    canvas = Canvas(api_url, api_key)

    # Get the course using the course ID
    course = canvas.get_course(course_id)

    # Get assignments from the course
    assignments = course.get_assignments()

    # Convert Canvas PaginatedList to a regular list of assignment dicts
    assignments_list = [assignment.__dict__ for assignment in assignments]

    # Return the list of assignments
    return {'assignments': assignments_list}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login credentials securely
        # Authenticate user and set session variables
        pass
    # Render login page
    return 'Login Page'

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use SSL/TLS to run the application

