from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Load configuration from environment variables or a separate config file
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = False  # Ensure debugging is disabled

# Initialize the database connection
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# Create the database tables
with app.app_context():
    db.create_all()

# Register URL
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # Check if the username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 409

    # Hash the password
    password_hash = generate_password_hash(password)

    # Create a new user and add to the database
    new_user = User(username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

if __name__ == '__main__':
    app.run()

