import secrets

def getSessionID():
    '''
    Return a random and unique session ID using the secrets module.
    '''
    # Generate a secure random session ID
    session_id = secrets.token_urlsafe()
    return session_id

# Example usage:
# session_id = getSessionID()
# print(session_id)

from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    # Disable debugging for production environment
    app.debug = False
    app.run()

