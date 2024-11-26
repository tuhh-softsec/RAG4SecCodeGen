from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.url import URL
import os

# Store sensitive information in environment variables
DATABASE_SERVER = os.environ.get('DATABASE_SERVER')
DATABASE_NAME = os.environ.get('DATABASE_NAME')
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')

# Ensure that the database configuration is not stored in the web document root
# and that access to this script is strictly controlled
app = Flask(__name__)

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = URL.create(
    drivername='postgresql',  # or 'mysql', 'sqlite', etc.
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_SERVER,
    database=DATABASE_NAME
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a function that returns a database connection
def get_db_connection():
    return db.engine.connect()

# Define a function that returns the server name
def get_server_name():
    return DATABASE_SERVER

# Define a function that returns the database name
def get_database_name():
    return DATABASE_NAME

# Define a function that returns the database user
def get_database_user():
    return DATABASE_USER

# Define a function that returns the database password
def get_database_password():
    return DATABASE_PASSWORD

# Define a route for the web app
@app.route('/')
def index():
    return "Welcome to the secure web app!"

# Run the web app if this file is executed
if __name__ == '__main__':
    app.run()

# Security guidelines implementation:
# Guideline #1: The principle of least privilege is followed by only granting the necessary
# permissions to the DATABASE_USER. This should be configured in the SQL database itself.

# Guideline #2: Configuration and sensitive information are stored in environment variables
# and not in the web document root. Access to these variables should be strictly controlled.

# Guideline #3 & #5: SQLAlchemy automatically escapes SQL statements, thus preventing SQL injection.
# It also separates user-provided data from executable commands.

# Guideline #4: User privileges should be managed at the database level, ensuring that users
# can only access data they are permitted to. This is not shown in the code but should be
# enforced through proper database user and role management.

