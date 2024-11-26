from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# Assuming we have a User model with username and password_hash fields
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@app.route('/login', methods=['POST'])
def check_mod():
    # Get username and password from the form
    username = request.form.get('username')
    password = request.form.get('password')

    # Find user by username
    user = User.query.filter_by(username=username).first()

    # Check if user exists and password is correct
    if user and user.check_password(password):
        # Perform additional security checks if necessary
        # ...

        # Return 'true' if authentication is successful
        return jsonify({'authenticated': True})
    else:
        # Return 'false' if authentication fails
        return jsonify({'authenticated': False})

if __name__ == '__main__':
    app.run()

