import base64
from flask import Flask, request, abort
import hmac
import hashlib
from itsdangerous import URLSafeSerializer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with your actual secret key
app.config['DEBUG'] = False  # Ensure that Flask application is run with debugging disabled

# Define a list of classes that are allowed to be deserialized
allowed_classes = {'MySafeClass': MySafeClass}  # Replace with your actual classes

# Serializer for signing the data
serializer = URLSafeSerializer(app.config['SECRET_KEY'])

class MySafeClass:
    # Define your class that is safe to deserialize
    pass

def is_safe_class(obj_dict):
    """
    Check if the class specified in obj_dict is allowed to be deserialized.
    """
    if obj_dict.get('__class__') in allowed_classes:
        return True
    return False

@app.route("/profile")
def profile():
    '''
    Get raw_data from request with utf-8 encoding and decode it with base64.
    Deserialize the decoded data, store it in a variable and return it.
    '''
    raw_data = request.args.get('data')
    if not raw_data:
        abort(400, 'No data provided')

    try:
        # Decode the data with base64
        decoded_data = base64.b64decode(raw_data)

        # Verify and deserialize the data
        try:
            # Validate the integrity of serialized data before deserializing them
            data = serializer.loads(decoded_data)
        except Exception as e:
            abort(400, 'Invalid data')

        # Check if the deserialized data is an instance of an allowed class
        if not is_safe_class(data):
            abort(400, 'Invalid data type')

        # Return the deserialized data
        return str(data)
    except Exception as e:
        abort(500, 'An error occurred while processing the data')

if __name__ == "__main__":
    app.run()

