from flask import Flask, request, make_response, abort
import lxml.etree
import os
import secrets

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Ensure Flask application is run with debugging disabled.

# Rate limiting setup
USER_REQUEST_LIMIT = 5
user_requests = {}

# Helper function to check and update request limits
def check_rate_limiting(ip):
    if ip in user_requests:
        requests_left, _ = user_requests[ip]
        if requests_left <= 0:
            abort(429)  # Too Many Requests
        user_requests[ip] = (requests_left - 1, secrets.token_urlsafe())
    else:
        user_requests[ip] = (USER_REQUEST_LIMIT - 1, secrets.token_urlsafe())

@app.before_request
def before_request():
    # Guideline #3: Prevent users from making further requests if their limit has been exceeded
    check_rate_limiting(request.remote_addr)

@app.post("/upload")
def upload():
    '''
    Get the xml_src from the request, parse it and return it as string.
    '''
    # Guideline #1: Verify if the pseudorandom value is present as a form value and a cookie value
    token_form = request.form.get('csrf_token')
    token_cookie = request.cookies.get('csrf_token')
    if not token_form or not token_cookie or token_form != token_cookie:
        abort(403)  # Forbidden

    # Guideline #2: Generate a pseudorandom value and set it as a cookie on the user's machine.
    response = make_response()
    csrf_token = secrets.token_urlsafe()
    response.set_cookie('csrf_token', csrf_token)

    # Guideline #7, #8, #9: Verify the type of files uploaded, ensure only one extension, and assign unique names
    uploaded_file = request.files.get('file')
    if uploaded_file:
        filename = uploaded_file.filename
        if '.' in filename and filename.rsplit('.', 1)[1].lower() in ['xml']:
            if filename.count('.') == 1:
                unique_filename = secrets.token_hex(8) + '.' + filename.rsplit('.', 1)[1]
                file_path = os.path.join('/path/to/upload/directory', unique_filename)
                uploaded_file.save(file_path)
                # Guideline #4, #5, #6: Execute the uploaded file with the lowest necessary privileges in a sandbox
                # Since we are only parsing XML, we do not execute the file, but we parse it securely.
                try:
                    with open(file_path, 'rb') as file:
                        xml_data = file.read()
                        parser = lxml.etree.XMLParser(resolve_entities=False)
                        tree = lxml.etree.fromstring(xml_data, parser=parser)
                        response.data = lxml.etree.tostring(tree)
                except lxml.etree.XMLSyntaxError as e:
                    abort(400, description="Invalid XML file.")
            else:
                abort(400, description="Invalid file extension.")
        else:
            abort(400, description="Unsupported file type.")
    else:
        abort(400, description="No file uploaded.")

    return response

if __name__ == "__main__":
    app.run()

