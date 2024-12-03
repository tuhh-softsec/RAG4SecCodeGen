from flask import Flask, request, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import ldap
import os

app = Flask(__name__)

# Load LDAP credentials and configuration from environment variables or a secure config file
LDAP_SERVER = os.environ.get('LDAP_SERVER', 'ldaps://localhost')  # Use LDAPS by default
LDAP_USE_SSL = os.environ.get('LDAP_USE_SSL', 'True').lower() in ['true', '1']
LDAP_BIND_DN = os.environ.get('LDAP_BIND_DN')
LDAP_BIND_PASSWORD = os.environ.get('LDAP_BIND_PASSWORD')

# Check if all required environment variables are set
required_env_vars = [LDAP_SERVER, LDAP_BIND_DN, LDAP_BIND_PASSWORD]
if not all(required_env_vars):
    raise ValueError("Missing one or more required environment variables.")

# Ensure that Flask application is run with security settings
app.config['DEBUG'] = False
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Set SameSite attribute for cookies

# Set up rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Set up secure headers
@app.after_request
def set_secure_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.route("/search")
@limiter.limit("10 per minute")  # Rate limit for the search endpoint
def search():
    # TODO: Implement authentication and authorization checks here

    # Get the Domain Component (dc) and username from the request
    # Sanitize and validate the input to prevent LDAP injection attacks
    dc = ldap.filter.escape_filter_chars(request.args.get('dc', ''))
    username = ldap.filter.escape_filter_chars(request.args.get('username', ''))

    # Ensure that the input is not empty and is valid
    if not dc or not username:
        return "Invalid input", 400

    # Create an LDAP query with sanitized inputs
    search_filter = f"(uid={username})"

    # Establish an LDAP connection
    try:
        # Initialize LDAP connection
        conn = ldap.initialize(LDAP_SERVER)
        conn.set_option(ldap.OPT_REFERRALS, 0)

        # Verify the server's certificate if using SSL
        if LDAP_USE_SSL:
            conn.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
            conn.start_tls_s()

        # Bind/authenticate with a user with appropriate rights to search
        conn.simple_bind_s(LDAP_BIND_DN, LDAP_BIND_PASSWORD)

        # Search for the user in the LDAP
        result = conn.search_s(f"dc={dc}", ldap.SCOPE_SUBTREE, search_filter)
        conn.unbind_s()

        # Return the search result
        return str(result)

    except ldap.LDAPError as e:
        # Log the error without sensitive information
        app.logger.error("LDAP connection or search failed: %s", str(e))

        # Return an error message without exposing details
        return "LDAP connection or search failed", 500

if __name__ == "__main__":
    # Use a production-ready WSGI server like Gunicorn or uWSGI in production
    app.run()

# Note: The LDAP credentials should be stored securely, not in the source code.
# They should be in environment variables or a secure config file with restricted access.
# Ensure that environment variables are not exposed in source code repositories or logging output.
# Ensure proper session management and TLS configuration for secure connections.
# Regularly audit security and update dependencies to protect against vulnerabilities.

