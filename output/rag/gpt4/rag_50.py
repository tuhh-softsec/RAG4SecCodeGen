from flask import Flask, request, make_response
import html

app = Flask(__name__)

# Assume that we have an authentication decorator that verifies the user is authenticated
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Implement authentication logic here
        # If not authenticated, return some error or redirect to login page
        return f(*args, **kwargs)
    return decorated

@app.route('/hello', methods=['GET'])
@requires_auth
def http_hello_page():
    # Guideline #5: Verify the origin of the request
    if 'Referer' not in request.headers or not is_valid_referer(request.headers['Referer']):
        return make_response('Invalid request origin', 403)

    # Guideline #3: Use a stringent allowlist for username
    username = request.args.get('username', '')
    if not is_valid_username(username):
        return make_response('Invalid username', 400)

    # Guideline #1: Do not reflect data directly back without proper encoding
    safe_username = html.escape(username)

    # Guideline #2: Specify encoding in the HTTP header
    response = make_response(f'Hello {safe_username}')
    response.headers['Content-Type'] = 'text/html; charset=utf-8'

    return response

def is_valid_referer(referer):
    # Implement logic to check if the referer is valid
    # For example, check if the referer is from the same domain
    return True

def is_valid_username(username):
    # Implement logic to check if the username is valid
    # For example, check against a regex pattern that only allows certain characters
    return True

if __name__ == '__main__':
    app.run()

