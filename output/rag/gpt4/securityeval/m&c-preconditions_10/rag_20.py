from flask import request, Flask
import ldap3
from ldap3.utils.dn import escape_rdn
import os

app = Flask(__name__)

# Load LDAP credentials and configuration from environment variables or a secure config file
LDAP_SERVER = os.environ.get('LDAP_SERVER', 'localhost')
LDAP_USE_SSL = True
LDAP_BIND_USER_DN = os.environ.get('LDAP_BIND_USER_DN')
LDAP_BIND_USER_PASSWORD = os.environ.get('LDAP_BIND_USER_PASSWORD')

# Ensure that Flask application is run with debugging disabled
app.config['DEBUG'] = False

@app.route("/normal")
def normal():
    # Ensure the requesting user is authorized to access this endpoint
    # This could be done with decorators or a manual check here
    # For example, using Flask-Login or a custom auth check

    # Get the Domain Component (dc) and username from the request
    # Ensure that input is properly escaped to prevent LDAP injection
    dc = escape_rdn(request.args.get('dc', ''))
    username = escape_rdn(request.args.get('username', ''))

    # Validate input to ensure it's not untrusted data
    if not dc or not username:
        return "Invalid input", 400

    # Establish an LDAP connection on localhost with SSL
    server = ldap3.Server(LDAP_SERVER, use_ssl=LDAP_USE_SSL)
    conn = ldap3.Connection(server, user=LDAP_BIND_USER_DN, password=LDAP_BIND_USER_PASSWORD, auto_bind=True)

    # Create an LDAP query with the escaped input
    search_filter = f"(uid={username})"
    search_base = f"dc={dc}"

    # Search for the user in the LDAP
    conn.search(search_base, search_filter, ldap3.SUBTREE)

    # Check if the user was found and return the result
    if conn.entries:
        user_data = conn.entries[0]
        return str(user_data)
    else:
        return "User not found", 404

if __name__ == "__main__":
    app.run()

# Remember to set the environment variables before running the application
# For example:
# export LDAP_BIND_USER_DN="cn=admin,dc=example,dc=com"
# export LDAP_BIND_USER_PASSWORD="yourpassword"

