from flask import request, Flask, jsonify
import ldap3
from ldap3.utils.dn import escape_rdn
import os
import ssl
from ldap3.core.exceptions import LDAPException
from config import load_config  # Assuming a secure config loader is implemented

app = Flask(__name__)

# Load LDAP credentials and configuration from a secure config file or secrets management tool
config = load_config()

LDAP_SERVER = config['LDAP_SERVER']
LDAP_USE_SSL = config['LDAP_USE_SSL']
LDAP_BIND_USER_DN = config['LDAP_BIND_USER_DN']
LDAP_BIND_USER_PASSWORD = config['LDAP_BIND_USER_PASSWORD']
CA_CERT_PATH = config['CA_CERT_PATH']  # Path to the CA certificate if using a custom CA

# Ensure that Flask debugging is disabled in production
app.config['DEBUG'] = False

# Set up secure TLS configuration with CA certificate validation
tls_configuration = ldap3.Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLS_CLIENT, ca_certs_file=CA_CERT_PATH)

@app.route("/normal")
def normal():
    # Authorization check should be implemented here
    # ...

    # Get the Domain Component (dc) and username from the request
    # Sanitize and validate the input to prevent LDAP injection attacks
    dc = escape_rdn(request.args.get('dc', ''))
    username = escape_rdn(request.args.get('username', ''))

    # Ensure that the input is not empty and is valid
    if not dc or not username:
        return "Invalid input", 400

    # Create an LDAP query with the sanitized input
    search_filter = f"(uid={username})"
    search_base = f"dc={dc}"

    try:
        # Establish an LDAP connection using SSL
        server = ldap3.Server(LDAP_SERVER, use_ssl=LDAP_USE_SSL, tls=tls_configuration)
        with ldap3.Connection(server, user=LDAP_BIND_USER_DN, password=LDAP_BIND_USER_PASSWORD, auto_bind=True) as conn:
            # Search for the user in the LDAP
            conn.search(search_base, search_filter, ldap3.SUBTREE)
            user_info = conn.entries

            # Filter out only necessary information before sending it to the client
            filtered_user_info = {attr.key: attr.value for attr in user_info[0].entry_attributes if attr.key in ['uid', 'cn', 'mail']}

            return jsonify(filtered_user_info)

    except LDAPException as e:
        # Log the exception without exposing sensitive information
        app.logger.error("An error occurred while connecting to LDAP.")
        return "An error occurred", 500

    except IndexError:
        return "User not found", 404

    except Exception as e:
        # Log the exception without exposing sensitive information
        app.logger.error("An unexpected error occurred.")
        return "An unexpected error occurred", 500

if __name__ == "__main__":
    # Run the Flask app with a production-ready server like Gunicorn or uWSGI
    # For example, using Gunicorn: gunicorn -w 4 'myapp:app'
    pass

# Note: It's important to ensure that the LDAP_BIND_USER_DN and LDAP_BIND_USER_PASSWORD
# are stored securely and not hard-coded. They should be stored in a secure configuration
# file with restricted access or retrieved from a secrets management tool.

