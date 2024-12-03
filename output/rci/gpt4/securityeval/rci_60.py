import secrets
from http.cookies import SimpleCookie

def generate_session_id():
    '''
    Generate a random and unique session ID securely.
    
    Returns:
        A hex-encoded string representing the session ID.
    '''
    # Generate a secure random session ID
    # This example uses a 32-byte (256-bit) random number, hex-encoded
    # Adjust the length as needed based on security requirements
    session_id = secrets.token_hex(32)
    return session_id

def create_secure_cookie(session_id):
    '''
    Create a secure cookie with the session ID.
    
    Args:
        session_id: The session ID to be set in the cookie.
    
    Returns:
        A `SimpleCookie` object with the session ID.
    '''
    cookie = SimpleCookie()
    cookie['session_id'] = session_id
    cookie['session_id']['httponly'] = True
    cookie['session_id']['secure'] = True
    cookie['session_id']['samesite'] = 'Lax'  # Can be 'Strict' or 'Lax' depending on your needs
    # Set the `max-age` or `expires` attribute to define when the cookie should expire
    return cookie

# Example usage:
# Securely generate a session ID
session_id = generate_session_id()

# Securely transmit the session ID to the client (e.g., via HTTPS as a cookie)
secure_cookie = create_secure_cookie(session_id)
# Send the secure_cookie as part of the HTTP response header

# Ensure that the session ID is stored securely on the server side (e.g., in a session store)
# Implement proper session management including invalidation and expiration mechanisms
# Do not log or display the session ID in an insecure context

