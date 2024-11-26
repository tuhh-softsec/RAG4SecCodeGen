from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, LargeBinary
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Generate a key for encrypting usernames. In a real-world scenario, you would want to store this key securely.
key = Fernet.generate_key()
cipher_suite = Fernet(key)

class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(LargeBinary)  # Encrypted username
    password_hash = Column(String(128))  # Hashed password

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_username(self, username):
        encrypted_username = cipher_suite.encrypt(username.encode('utf-8'))
        self.username = encrypted_username

    def get_username(self):
        return cipher_suite.decrypt(self.username).decode('utf-8')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Check if the user already exists
    user = User.query.filter_by(username=cipher_suite.encrypt(username.encode('utf-8'))).first()
    if user:
        return jsonify({'message': 'User already exists'}), 400

    # Create a new user with encrypted username and hashed password
    new_user = User()
    new_user.set_username(username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Find user by encrypted username
    user = User.query.filter_by(username=cipher_suite.encrypt(username.encode('utf-8'))).first()
    if user and user.check_password(password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)

