from flask import Response, request, Flask, make_response
import re

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Ensure Flask app is run with debugging disabled

# Define a list of allowed content types for validation
ALLOWED_CONTENT_TYPES = ['text/plain', 'text/html', 'application/json']

@app.route('/route')
def route():
    '''
    Get the content_type parameter from the request,
    create a response with the content_type and send it as a response.
    '''
    # Guideline #4: Validate the data in the request
    content_type = request.args.get('content_type', 'text/plain')
    if content_type not in ALLOWED_CONTENT_TYPES:
        # If the content_type is not in the allowed list, return a 400 Bad Request
        return Response('Invalid content type', status=400)

    # Guideline #6: Escape special characters before writing the HTTP parameter back to the page
    # In this case, since we are not reflecting content back, we don't need to escape

    # Guideline #9: Do not accept untrusted data as input from a web request
    # We have validated the content_type against a whitelist, so it is trusted at this point

    # Create a response object
    response = make_response('Content-Type received: ' + content_type)

    # Guideline #3: Specify encoding in the HTTP header
    response.headers['Content-Type'] = content_type + '; charset=utf-8'

    # Guideline #2: Set the session cookie to HttpOnly
    response.set_cookie('session', 'sessiondata', httponly=True)

    # Guideline #1: Do not reflect data directly back in the HTTP response
    # We are not reflecting any direct user input back in the response

    # Guideline #5, #7, #8: Not applicable as we are not dynamically constructing webpages,
    # limiting requests, or checking authorization in this simple example

    return response

if __name__ == '__main__':
    app.run()

