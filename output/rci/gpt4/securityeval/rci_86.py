from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_ipaddr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash
import os
import re

app = Flask(__name__)

# Use environment variables for sensitive data
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Implement rate limiting with a key function that works behind a reverse proxy
limiter = Limiter(
    app,
    key_func=get_ipaddr,
    default_limits=["5 per minute"]
)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Register URL
@app.route('/register', methods=['POST'])
@limiter.limit("3 per minute")  # More strict rate limit for registration
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    # Enforce password complexity
    if not username or not password or not username.isalnum() or len(password) < 8 or not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
        return jsonify({"error": "Invalid input"}), 400

    # Hash the password with a specified algorithm
    hashed_password = generate_password_hash(password, method='bcrypt')

    try:
        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            # Use a generic error message
            return jsonify({"error": "Registration failed"}), 400

        # Insert new user into the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        # Use a generic error message
        return jsonify({"error": "An error occurred"}), 500

    # Use a generic success message
    return jsonify({"message": "Registration completed"}), 201

# Additional security configurations (not shown in the code):
# - Set up a proper SSL/TLS certificate for HTTPS.
# - Implement CSRF protection using Flask-WTF or similar extension.
# - Define a Content Security Policy header.
# - Use a connection pool for database connections.
# - Ensure sensitive data is not logged.
# - Implement account lockout mechanism after several failed login attempts.
# - Set security-related HTTP headers.
# - Regularly update dependencies to their latest secure versions.
# - Ensure the `DATABASE_URL` is not logged or exposed.
# - Deploy the application using a production-ready WSGI server and a reverse proxy.

if __name__ == '__main__':
    # Do not run the app directly in production
    pass

