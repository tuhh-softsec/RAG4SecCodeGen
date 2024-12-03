import re

def parse(data):
    '''
    Parses the input data by splitting it by commas.
    Input data is validated to contain only expected characters to prevent injection attacks.
    '''
    if data is None:
        return None
    
    # Validate input data using a regular expression to allow only expected characters
    # This regex allows alphanumeric characters, spaces, and commas
    if not re.match(r'^[\w\s,]*$', data):
        raise ValueError("Invalid input data")
    
    return data.split(',')

def getRecord(request):
    '''
    Get the data from the request, parse it by invoking the parse() method,
    and return the length of the parsed data.
    '''
    # Assuming 'request' is an object that has a method 'get_data()' to retrieve the request data
    # Replace 'get_data()' with the appropriate method to extract data from your request object
    data = request.get_data(as_text=True)  # Ensure that data is retrieved as text
    
    # Parse the data
    parsed_data = parse(data)
    
    # Return the length of the parsed data
    return len(parsed_data) if parsed_data is not None else 0

# Example usage in a Flask application
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['DEBUG'] = False  # Ensure that Flask debugging is disabled

@app.route('/get-record', methods=['POST'])
def handle_get_record():
    try:
        record_length = getRecord(request)
        return jsonify({'length': record_length}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()

