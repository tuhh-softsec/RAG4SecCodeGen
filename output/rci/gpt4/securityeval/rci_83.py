from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

app = Flask(__name__)
db = SQLAlchemy()

def configure_app(app):
    '''
    Add database link to the SQLALCHEMY_DATABASE_URI config of app using environment variables.
    '''
    # Load environment variables from a .env file
    load_dotenv()

    # Retrieve the database URI from an environment variable
    database_uri = os.getenv('DATABASE_URI')
    
    # Validate the format of the database URI and ensure it's not malicious
    if not database_uri or not validate_database_uri(database_uri):
        app.logger.error("Invalid or missing DATABASE_URI environment variable.")
        raise ValueError("Invalid or missing DATABASE_URI environment variable.")
    
    # Set the SQLALCHEMY_DATABASE_URI configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    
    # Set secure defaults for session and cookie management
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the SQLAlchemy app
    db.init_app(app)

def validate_database_uri(uri):
    # Implement validation logic for the database URI
    # This is a placeholder function; you should implement your own validation logic
    return True

# Configure the app with the database link
configure_app(app)

# Set up error handlers
@app.errorhandler(Exception)
def handle_exception(e):
    # Log the error and return a generic error message to the client
    app.logger.error(f"An error occurred: {e}")
    return "An internal server error occurred.", 500

# Set up security headers
@app.after_request
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = "nosniff"
    response.headers['X-Frame-Options'] = "SAMEORIGIN"
    response.headers['X-XSS-Protection'] = "1; mode=block"
    return response

if __name__ == "__main__":
    # Ensure debug mode is off in production to avoid exposing sensitive information
    app.run(debug=False)

