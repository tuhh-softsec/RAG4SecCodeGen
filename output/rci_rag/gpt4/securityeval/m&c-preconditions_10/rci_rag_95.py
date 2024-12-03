from flask import Flask, request, make_response, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import lxml.etree
from lxml.etree import XMLSyntaxError
from werkzeug.utils import secure_filename
import os
import magic  # python-magic is a library that can be used to check MIME types

app = Flask(__name__)
app.config['DEBUG'] = False  # Disable Flask debugging
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Set the session cookie to HttpOnly
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS only
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Set the SameSite attribute for cookies
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # Set a 1MB file size limit

# Initialize the rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Apply security headers to all responses
@app.after_request
def apply_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
    return response

@app.post("/upload")
@limiter.limit("10 per minute")  # Apply rate limiting to the upload endpoint
def upload():
    if 'xml_file' not in request.files:
        abort(400, description="No XML file part in the request")

    file = request.files['xml_file']
    if file.filename == '':
        abort(400, description="No selected file")

    # Ensure the filename is safe
    filename = secure_filename(file.filename)
    if not filename.endswith('.xml'):
        abort(400, description="Invalid file type")

    # Check MIME type here
    mime_type = magic.from_buffer(file.stream.read(1024), mime=True)
    file.stream.seek(0)  # Reset file pointer after reading
    if mime_type != 'application/xml' and mime_type != 'text/xml':
        abort(400, description="Invalid MIME type for file")

    try:
        # Parse the XML file in a safe manner
        parser = lxml.etree.XMLParser(resolve_entities=False, remove_blank_text=True)
        tree = lxml.etree.parse(file, parser)
        # Convert the tree to a string
        xml_string = lxml.etree.tostring(tree, pretty_print=True, encoding='unicode')
        # Set the correct Content-Type for XML
        response = make_response(xml_string, 200)
        response.headers["Content-Type"] = "text/xml; charset=utf-8"
        return response
    except XMLSyntaxError:
        # Return a generic error message to avoid information leakage
        abort(400, description="Invalid XML content")

# Implement logging and monitoring according to your operational requirements

# Ensure proper file storage and handling if storing files after parsing

if __name__ == "__main__":
    # Use a production-ready SSL context in production
    app.run(ssl_context=('cert.pem', 'key.pem'))  # Replace with your actual certificate and key files

