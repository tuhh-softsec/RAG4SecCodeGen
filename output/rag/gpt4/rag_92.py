from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import re

app = Flask(__name__)

# Function to validate input parameters
def validate_input(latitude, longitude, year, month, day, grib_file):
    try:
        lat = float(latitude)
        lon = float(longitude)
        yr = int(year)
        mo = int(month)
        dy = int(day)
        if not (re.match(r'^[\w\-.]+$', grib_file) and len(grib_file) <= 255):
            raise ValueError("Invalid grib_file format.")
        return lat, lon, yr, mo, dy
    except ValueError as e:
        return None

# Function to get the maximum temperature from the database
def get_max_temperature(latitude, longitude, year, month, day, grib_file):
    try:
        connection = mysql.connector.connect(
            host='your_host',
            database='your_database',
            user='your_user',
            password='your_password'
        )
        cursor = connection.cursor(prepared=True)
        query = """
        SELECT MAX(temperature) FROM weather_data
        WHERE latitude = %s AND longitude = %s AND year = %s AND month = %s AND day = %s AND grib_file = %s
        """
        cursor.execute(query, (latitude, longitude, year, month, day, grib_file))
        result = cursor.fetchone()
        return result[0] if result else None
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/temperature_for_location', methods=['GET'])
def temperature_for_location():
    # Apply authentication before returning the requested data
    # This is a placeholder for actual authentication logic
    if not request.headers.get('Authorization'):
        return jsonify({"error": "Unauthorized"}), 401

    # Validate and extract parameters
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    grib_file = request.args.get('grib_file')

    # Validate input
    validated_input = validate_input(latitude, longitude, year, month, day, grib_file)
    if not validated_input:
        return jsonify({"error": "Invalid input parameters"}), 400

    # Get the maximum temperature
    max_temp = get_max_temperature(*validated_input)
    if max_temp is None:
        return jsonify({"error": "Data not found"}), 404

    # Specify encoding in the HTTP header
    response = jsonify({"max_temperature": max_temp})
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

if __name__ == '__main__':
    app.run(debug=True)

