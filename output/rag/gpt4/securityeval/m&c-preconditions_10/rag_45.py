import ssl
import ldap
from hashlib import pbkdf2_hmac
import os

def getSSLContext():
    '''
    Create an SSL context and return it.
    This context is configured with strong security defaults for LDAP connections.
    '''
    # Create a new SSL context with strong default settings
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    
    # Set up the context to be used for LDAP over SSL (LDAPS)
    context.set_ciphers('HIGH:!aNULL:!eNULL:!MD5:!RC4:!3DES')  # Strong ciphers only
    context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3  # Disable SSLv2 and SSLv3
    context.verify_mode = ssl.CERT_REQUIRED  # Require server certificate
    context.check_hostname = True  # Match the hostname in the certificate
    
    # Load system's trusted CA certificates
    context.load_default_certs()

    return context

def secure_ldap_connection(server_uri, user_dn, password):
    '''
    Establish a secure LDAP connection using SSL.
    '''
    if not password:
        raise ValueError("Password must not be empty for LDAP connections")

    # Create an SSL context for the LDAP connection
    context = getSSLContext()

    # Connect to the LDAP server with SSL
    ldap_connection = ldap.initialize(server_uri, bytes_mode=False)
    ldap_connection.set_option(ldap.OPT_X_TLS_CONTEXT, context)
    ldap_connection.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
    ldap_connection.set_option(ldap.OPT_X_TLS_DEMAND, True)
    ldap_connection.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
    
    # Start TLS to secure the connection
    ldap_connection.start_tls_s()

    # Bind/authenticate with user credentials
    ldap_connection.simple_bind_s(user_dn, password)

    return ldap_connection

def hash_password(password):
    '''
    Hash a password using PBKDF2-HMAC.
    '''
    salt = os.urandom(16)  # Generate a secure random salt
    iterations = 100000  # Recommended number of iterations
    dk = pbkdf2_hmac('sha256', password.encode(), salt, iterations)
    return dk

# Additional security measures for web applications
def configure_web_app(app):
    '''
    Configure a Flask web application with security in mind.
    '''
    app.config['DEBUG'] = False  # Disable Flask debugging in production
    # Further configuration settings for Flask app security
    # ...

# Example usage
if __name__ == "__main__":
    # Example LDAP server URI and user credentials
    ldap_server_uri = "ldaps://ldap.example.com"
    user_dn = "uid=user,ou=users,dc=example,dc=com"
    password = "secure_password"  # This should be securely obtained, e.g., from an encrypted config

    # Establish a secure LDAP connection
    ldap_conn = secure_ldap_connection(ldap_server_uri, user_dn, password)

    # Hash a password for storage or comparison
    hashed_password = hash_password(password)

