from flask import Flask, request, jsonify
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os

app = Flask(__name__)

# Configure database connection (example with PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/Sensor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Configure caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Set up the cache timeout (in seconds)
CACHE_TIMEOUT = 300

# Function to get temperature for a location
@app.route('/api/temperature_for_location', methods=['POST'])
def temperature_for_location():
    # Validate and parse the input data
    try:
        payload = request.get_json()
        latitude = float(payload['latitude'])
        longitude = float(payload['longitude'])
        date = payload['date']
    except (ValueError, KeyError, TypeError):
        return jsonify({"error": "Invalid input data"}), 400

    # Create a cache key based on the input parameters
    cache_key = f"temperature_{latitude}_{longitude}_{date}"

    # Try to get the cached result
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return jsonify({"temperature": cached_result}), 200

    # Use a parameterized query to prevent SQL injection
    query = text("SELECT temperature FROM temperature_data WHERE latitude = :latitude AND longitude = :longitude AND date = :date")
    result = db.engine.execute(query, latitude=latitude, longitude=longitude, date=date).fetchone()

    # Check if the result is found
    if result is None:
        return jsonify({"error": "Temperature data not found"}), 404

    # Cache the result
    cache.set(cache_key, result[0], timeout=CACHE_TIMEOUT)

    # Return the temperature
    return jsonify({"temperature": result[0]}), 200

# Set the encoding in the HTTP header
@app.after_request
def set_encoding(response):
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

# Require authentication for accessing the API
@app.before_request
def require_auth():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return jsonify({"error": "Authentication required"}), 401

def check_auth(username, password):
    # Implement your authentication logic here
    # For example, check against environment variables
    return username == os.getenv('API_USER') and password == os.getenv('API_PASSWORD')

if __name__ == '__main__':
    app.run(debug=False)

