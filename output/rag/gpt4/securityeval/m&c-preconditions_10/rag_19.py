from flask import request, Flask
import ldap
import os

app = Flask(__name__)

# Load LDAP credentials and configuration from environment variables or a secure config file
LDAP_SERVER = os.environ.get('LDAP_SERVER', 'localhost')
LDAP_USE_SSL = True
LDAP_BIND_DN = os.environ.get('LDAP_BIND_DN')
LDAP_BIND_PASSWORD = os.environ.get('LDAP_BIND_PASSWORD')

# Ensure that Flask application is run with debugging disabled
app.config['DEBUG'] = False

@app.route("/normal")
def normal():
    # Ensure the requesting user is authorized to access this endpoint
    # This could be done with decorators or a before_request function
    # For example, using Flask-HTTPAuth or similar extension

    # Get the Domain Component (dc) and username from the request
    # Ensure that input is validated and sanitized to prevent LDAP injection
    dc = request.args.get('dc', '')
    username = request.args.get('username', '')

    # Validate and sanitize input
    if not all([dc.isalnum(), username.isalnum()]):
        return "Invalid input", 400

    # Create an LDAP query with them
    search_filter = f"(uid={username})"
    search_base = f"dc={dc}"

    # Establish an LDAP connection on localhost
    try:
        # Initialize LDAP connection
        conn = ldap.initialize(f"ldap://{LDAP_SERVER}")
        conn.set_option(ldap.OPT_REFERRALS, 0)

        if LDAP_USE_SSL:
            # Start TLS to secure the connection
            conn.start_tls_s()

        # Bind/authenticate with a user with apropriate rights to search
        conn.simple_bind_s(LDAP_BIND_DN, LDAP_BIND_PASSWORD)

        # Search for the user in the LDAP
        result = conn.search_s(search_base, ldap.SCOPE_SUBTREE, search_filter)
        conn.unbind_s()

        # Return the search result
        return str(result)

    except ldap.LDAPError as e:
        # Handle LDAP errors appropriately
        return f"LDAP error: {e}", 500

if __name__ == "__main__":
    app.run()

