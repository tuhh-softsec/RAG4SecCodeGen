from flask import Flask, request, abort
from lxml import etree
import re

app = Flask(__name__)

# Configure Flask to not run in debug mode in production
app.config.update(
    DEBUG=False,
    ENV='production',
    # Secure session cookie configuration
    SECRET_KEY='your-random-secret-key',  # Replace with a real random key
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',  # or 'Strict' depending on your requirements
    # Additional security-related configuration settings
)

# Define a function to parse the Content-Type header
def parse_content_type(content_type):
    if content_type:
        content_type, *params = content_type.split(';')
        return content_type.lower().strip()
    return None

@app.post("/upload")
def upload():
    '''
    Get the xml_src from the request, parse it securely, and return it as a string.
    '''
    # Parse and check the Content-Type of the incoming request
    content_type = parse_content_type(request.headers.get('Content-Type'))
    if content_type not in ['application/xml', 'text/xml']:
        abort(415, description="Unsupported Media Type. Please send XML data.")

    # Get the XML data from the request
    xml_src = request.data

    if not xml_src:
        abort(400, description="No XML data provided.")

    try:
        # Parse the XML securely with additional settings to prevent XXE and DoS attacks
        parser = etree.XMLParser(
            resolve_entities=False,
            no_network=True,
            dtd_validation=False,
            huge_tree=False,
            remove_blank_text=True
        )
        root = etree.fromstring(xml_src, parser=parser)

        # Validate the XML against a known schema (if applicable)
        # schema = etree.XMLSchema(etree.parse('your-schema.xsd'))
        # schema.assertValid(root)

        # Convert the XML tree back to a string, ensuring proper encoding
        xml_string = etree.tostring(root, pretty_print=True, encoding='unicode')

        # Sanitize or encode the data if it is intended for display in a web browser

        return xml_string
    except (etree.XMLSyntaxError, etree.DocumentInvalid) as e:
        # Return a generic error message to avoid information disclosure
        abort(400, description="XML parsing error.")

    # Additional error handling can be implemented as needed

# Implement rate limiting (example using Flask-Limiter)
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
# limiter = Limiter(
#     app,
#     key_func=get_remote_address,
#     default_limits=["200 per day", "50 per hour"]
# )

if __name__ == "__main__":
    # Ensure that the application is not serving on a publicly accessible IP address or port unless properly secured
    app.run(host='127.0.0.1', port=5000)

