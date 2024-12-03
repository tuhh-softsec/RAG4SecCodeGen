from flask import Flask, request, jsonify, abort
import ldap3
from ldap3.utils.dn import escape_rdn
import os
import logging
from ldap3.core.exceptions import LDAPException
from flask_login import LoginManager  # For session management
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Configure logging to avoid exposing sensitive data
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load LDAP server configuration from environment variables or a secrets manager
LDAP_SERVER = os.getenv('LDAP_SERVER', 'localhost')
LDAP_PORT = int(os.getenv('LDAP_PORT', 389))  # Default LDAP port for StartTLS
LDAP_USE_SSL = os.getenv('LDAP_USE_SSL', 'False') == 'True'
LDAP_BIND_USER = os.getenv('LDAP_BIND_USER')
LDAP_BIND_PASSWORD = os.getenv('LDAP_BIND_PASSWORD')
CA_CERT_PATH = os.getenv('CA_CERT_PATH')  # Path to the CA certificate

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Ensure SSL/TLS certificate paths are set and valid
SSL_KEY_PATH = os.getenv('SSL_KEY_PATH')
SSL_CERT_PATH = os.getenv('SSL_CERT_PATH')
if not SSL_KEY_PATH or not SSL_CERT_PATH or not os.path.exists(SSL_KEY_PATH) or not os.path.exists(SSL_CERT_PATH):
    logging.error("SSL key or certificate path is invalid.")
    raise FileNotFoundError("SSL key or certificate path is invalid.")

# Set up security headers
@app.after_request
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = "nosniff"
    response.headers['X-Frame-Options'] = "SAMEORIGIN"
    response.headers['Strict-Transport-Security'] = "max-age=63072000; includeSubDomains"
    return response

@app.route("/search")
def search():
    # Get the Domain Component (dc) and username from the request
    dc = request.args.get('dc')
    username = request.args.get('username')

    # Validate and sanitize the input
    if not dc or not username:
        abort(400, description="Missing dc or username parameter")

    # Escape the input to prevent LDAP injection attacks
    dc_escaped = escape_rdn(dc)
    username_escaped = escape_rdn(username)

    # Create an LDAP query with the escaped values
    search_filter = f"(uid={username_escaped})"
    search_base = f"dc={dc_escaped}"

    # Establish an LDAP connection
    server = ldap3.Server(LDAP_SERVER, port=LDAP_PORT, use_ssl=LDAP_USE_SSL, get_info=ldap3.ALL, tls=ldap3.Tls(ca_certs_file=CA_CERT_PATH))
    conn = None
    try:
        conn = ldap3.Connection(server, user=LDAP_BIND_USER, password=LDAP_BIND_PASSWORD, auto_bind=True)
        if LDAP_USE_SSL and LDAP_PORT == 389:
            # Start TLS session if using StartTLS on port 389
            conn.start_tls()

        # Search for the user in the LDAP
        conn.search(search_base, search_filter, ldap3.SUBTREE)
        # Check if the search was successful
        if not conn.entries:
            return jsonify({"error": "User not found"}), 404

        # Return the user's LDAP entry
        user_info = conn.entries[0].entry_to_json()
        return jsonify({"user": user_info})

    except LDAPException as e:
        # Log the actual error and return a generic error message
        logging.error(f"LDAPException occurred: {e}")
        return jsonify({"error": "An error occurred while processing your request"}), 500

    finally:
        # Check if the connection is bound before attempting to unbind
        if conn and conn.bound:
            conn.unbind()

if __name__ == "__main__":
    # Use a production-ready WSGI server instead of the development server
    from gunicorn.app.base import BaseApplication

    class FlaskApplication(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {key: value for key, value in self.options.items()
                      if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    options = {
        'bind': '%s:%s' % ('127.0.0.1', '443'),  # Bind to localhost for security
        'workers': int(os.getenv('GUNICORN_WORKERS', 4)),
        'keyfile': SSL_KEY_PATH,
        'certfile': SSL_CERT_PATH,
    }
    FlaskApplication(app, options).run()

