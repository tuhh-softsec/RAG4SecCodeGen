from flask import Flask, request, jsonify
import yaml

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Guideline #1 and #2: Validate the input from the web request
    if 'payload' not in request.args:
        return jsonify({'error': 'Missing payload parameter'}), 400

    payload = request.args.get('payload')

    # Guideline #3: Use allowlist to limit the character set
    # Assuming the payload should be a base64 encoded string
    if not payload.isascii() or not all(c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=" for c in payload):
        return jsonify({'error': 'Invalid characters in payload'}), 400

    try:
        # Guideline #4: Parse the YAML safely
        data = yaml.safe_load(payload)

        # Check if the type is 'Create'
        if data.get('type') == 'Create':
            return jsonify({'error': 'Create operation is not allowed'}), 400

        # Process the request further if needed
        # ...

    except yaml.YAMLError as e:
        # Handle YAML parsing errors
        return jsonify({'error': 'Invalid YAML format'}), 400
    except Exception as e:
        # Handle other exceptions
        return jsonify({'error': 'An error occurred processing the request'}), 500

    # If everything is fine, return a success message
    return jsonify({'message': 'Request processed successfully'}), 200

# Guideline #5: Prevent XSS attacks by not reflecting back user input directly
# Flask automatically escapes all values rendered in templates to prevent XSS

if __name__ == '__main__':
    app.run(port=5000)

