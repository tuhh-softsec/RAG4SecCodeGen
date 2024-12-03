from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import MySQLdb
import os
from flask_talisman import Talisman

app = Flask(__name__)

# Load configuration from environment variables or a separate config file
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')

# Ensure that Flask application is run with debugging disabled
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
if not app.config['SECRET_KEY']:
    raise ValueError("No SECRET_KEY set for Flask application")

app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Security headers with Flask-Talisman
talisman = Talisman(app)

# Rate limiter configuration
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)

# Database connection function
def get_db_connection():
    conn = MySQLdb.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASS,
        db=DB_NAME,
        ssl={
            'ca': os.environ.get('DB_SSL_CA'),
            'cert': os.environ.get('DB_SSL_CERT'),
            'key': os.environ.get('DB_SSL_KEY')
        }
    )
    return conn

# Register URL with rate limiting
@app.route('/register', methods=['POST'])
@limiter.limit("2 per minute")
def register():
    '''
    Get username and password from the request, and check if the username is already in the database.
    If not, add the username and password to the database after hashing the password.
    '''
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validate input
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    # TODO: Implement password complexity requirements and validation here

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if the username already exists
        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            # Avoid giving away information on whether a username exists
            return jsonify({'message': 'Registration attempt received'}), 200

        # Insert new user into the database
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
        conn.commit()

        return jsonify({'message': 'Registration successful'}), 201
    except MySQLdb.Error as e:
        # Log the error internally without exposing sensitive information
        app.logger.error(f'Database error: {e}')
        return jsonify({'message': 'An error occurred'}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    # In production, specify the path to the SSL certificate and key.
    # For development, you can use 'adhoc' but ensure it's not used in production.
    ssl_context = ('/path/to/ssl.cert', '/path/to/ssl.key') if not app.debug else 'adhoc'
    app.run(ssl_context=ssl_context)

