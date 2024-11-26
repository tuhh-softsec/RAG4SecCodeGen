from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_httpauth import HTTPBasicAuth
import re
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temperature.db'  # Replace with your database URI
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

# Basic authentication setup
users = {
    "user1": "password1",  # Replace with real user credentials
    # Add other users here
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

# Temperature model
class Temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    temperature = db.Column(db.Float, nullable=False)

@app.route('/api/temperature_for_location', methods=['GET'])
@auth.login_required
def temperature_for_location():
    # Validate and extract parameters
    try:
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        date_str = request.args.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid parameters"}), 400

    # Use a prepared statement to prevent SQL injection
    result = Temperature.query.filter(
        func.round(Temperature.latitude, 6) == round(latitude, 6),
        func.round(Temperature.longitude, 6) == round(longitude, 6),
        Temperature.date == date
    ).first()

    # Return the result
    if result:
        return jsonify({"temperature": result.temperature})
    else:
        return jsonify({"error": "Temperature data not found"}), 404

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use SSL/TLS for secure communication

