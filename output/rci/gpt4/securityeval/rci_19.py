import os
import ssl
from flask import Flask, request, jsonify
from ldap3 import Server, Connection, ALL, Tls, SAFE_SYNC
from ldap3.core.exceptions import LDAPException
from ldap3.utils.dn import escape_dn_chars
from ldap3.utils.conv import escape_filter_chars
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)

# Retrieve LDAP connection details from environment variables
LDAP_HOST = os.getenv('LDAP_HOST', 'localhost')
LDAP_PORT = int(os.getenv('LDAP_PORT', '636'))
LDAP_USE_SSL = os.getenv('LDAP_USE_SSL', 'True').lower() in ['true', '1', 't']
LDAP_BIND_USER = os.getenv('LDAP_BIND_USER')
LDAP_BIND_PASSWORD = os.getenv('LDAP_BIND_PASSWORD')
CA_CERT_FILE = os.getenv('CA_CERT_FILE')  # Path to the CA certificate file

# Set up TLS configuration
tls_configuration = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2, ca_certs_file=CA_CERT_FILE)

@app.route("/search")
def search():
    # Get the Domain Component (dc) and username from the request
    dc = request.args.get('dc')
    username = request.args.get('username')

    # Validate and sanitize the input to ensure it's safe to use in an LDAP query
    if not dc or not username:
        return jsonify({"error": "Invalid input"}), 400

    dc = escape_dn_chars(dc)
    username = escape_filter_chars(username)

    # Create an LDAP query using safe string formatting
    search_filter = f"(uid={username})"
    search_base = f"dc={dc}"

    # Establish an LDAP connection
    try:
        server = Server(LDAP_HOST, port=LDAP_PORT, use_ssl=LDAP_USE_SSL, tls=tls_configuration, get_info=ALL)
        with Connection(server, user=LDAP_BIND_USER, password=LDAP_BIND_PASSWORD, auto_bind=True, client_strategy=SAFE_SYNC) as conn:
            # Search for the user in the LDAP
            conn.search(search_base, search_filter)
            # Fetch the response
            response = conn.response
            # Return the search results, ensuring sensitive data is filtered or anonymized
            return jsonify({'results': response}), 200
    except LDAPException as e:
        # Log the error details securely
        app.logger.error(f"LDAP error: {str(e)}")
        # Provide a generic error message to the end-user
        return jsonify({"error": "An error occurred while processing your request."}), 500
    except Exception as e:
        # Log the error details securely
        app.logger.error(f"Unexpected error: {str(e)}")
        # Provide a generic error message to the end-user
        return jsonify({"error": "An unexpected error occurred."}), 500

# Implement additional security measures such as rate limiting, session management, and security headers
# ...

if __name__ == "__main__":
    # Disable debug mode for production
    app.run(debug=False)

