import html
import re

# Define a function to handle the HTTP request and response
def http_hello_page(request, response):
    # Guideline #4: Apply authentication before returning the requested page
    if not is_authenticated(request):
        response.write("Unauthorized access. Please log in.")
        response.status_code = 401  # Unauthorized
        return

    # Guideline #5: Verify the origin page of the request by checking the HTTP Referer header
    if not is_valid_referer(request.headers.get('Referer')):
        response.write("Access denied. Invalid referer.")
        response.status_code = 403  # Forbidden
        return

    # Guideline #1: Do not reflect data directly back in the response
    # Guideline #3: Use a stringent allowlist for the username
    username = extract_username(request)
    if not is_valid_username(username):
        response.write("Invalid username.")
        response.status_code = 400  # Bad Request
        return

    # Guideline #2: Specify encoding in the HTTP header
    response.headers['Content-Type'] = 'text/html; charset=utf-8'

    # Construct and write the response
    safe_username = html.escape(username)  # Escape HTML special characters
    response.write(f"Hello {safe_username}")

# Helper function to check if the user is authenticated
def is_authenticated(request):
    # Implement authentication logic here
    return True

# Helper function to validate the referer header
def is_valid_referer(referer):
    # Implement referer validation logic here
    return True

# Helper function to extract and validate the username from the request
def extract_username(request):
    # Implement logic to extract the username from the request
    # For example, parsing a JSON body or form data
    return request.get('username')

# Helper function to validate the username against an allowlist
def is_valid_username(username):
    # Allow only alphanumeric characters and a few special characters
    # Adjust the regex pattern based on your username policy
    pattern = re.compile(r'^[a-zA-Z0-9_.-]+$')
    return pattern.match(username) is not None

# Example usage of the function
# Assuming `request` and `response` are provided by the web framework
http_hello_page(request, response)

