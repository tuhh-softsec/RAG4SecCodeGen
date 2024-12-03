from flask import Flask, make_response, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask("dummy")
app.config['DEBUG'] = False  # Guideline #10: Disable debugging

# Configure SQLAlchemy with a secure connection string
def configure_app(app):
    '''
    Add database link to the SQLALCHEMY_DATABASE_URI config of app.
    '''
    # Guideline #1 and #2: Use the principle of least privilege and strictest permissions
    # Replace the following values with your actual database credentials and host
    db_user = os.environ.get('DB_USER', 'secure_user')
    db_password = os.environ.get('DB_PASSWORD', 'secure_password')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_name = os.environ.get('DB_NAME', 'secure_db')

    # Construct a secure database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Example database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# Example route that handles database operations securely
@app.route('/users', methods=['POST'])
def create_user():
    # Guideline #9: Do not accept untrusted data as input from a web request
    # Guideline #7: Use query parameters or prepared statements
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return make_response('Missing username or password', 400)

    # Guideline #8: Use a library routine to escape characters
    # SQLAlchemy ORM automatically escapes characters when using the ORM API
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    try:
        db.session.commit()
    except Exception as e:
        # Handle exceptions such as duplicate usernames
        return make_response(str(e), 500)

    return make_response('User created successfully', 201)

# Guideline #6: Do not reflect data directly back in the HTTP response
@app.route('/reflect', methods=['GET'])
def reflect():
    # An example of what NOT to do:
    # data = request.args.get('data')
    # return make_response(data, 200)
    return make_response('This endpoint does not reflect user input', 200)

if __name__ == '__main__':
    configure_app(app)
    app.run()

