from flask import Flask, request, Response
import yaml
import re

app = Flask(__name__)

# Assuming this function is secure and uses parameterized queries to prevent SQL injection
def get_price_for_product_code(product_code):
    # Implementation that retrieves the price for the given product code from the database
    pass

# Helper function to sanitize output for YAML to prevent any potential code injection
def sanitize_yaml_output(data):
    # Encode all non-alphanumeric characters
    return re.sub(r'([^a-zA-Z0-9])', lambda x: f"\\{x.group(1)}", str(data))

@app.route('/calculate_price', methods=['GET'])
def calculate_price():
    try:
        # Load the YAML payload from the query parameter
        yaml_payload = request.args.get('payload', '')
        data = yaml.safe_load(yaml_payload)  # Use safe_load to prevent code execution

        # Extract product code and quantity from the data dictionary
        product_code = data.get('product_code')
        quantity = data.get('quantity', 1)

        # Validate and sanitize inputs
        if not isinstance(product_code, str) or not isinstance(quantity, int):
            return Response("Invalid input", status=400)

        # Calculate the total price
        price_per_unit = get_price_for_product_code(product_code)
        total_price = price_per_unit * quantity

        # Prepare the YAML response
        response_data = {
            'total_price': sanitize_yaml_output(total_price)
        }
        yaml_response = yaml.dump(response_data)

        # Return the response with proper content-type
        return Response(yaml_response, mimetype='application/x-yaml')

    except yaml.YAMLError as e:
        # Handle YAML errors
        return Response("Invalid YAML format", status=400)
    except Exception as e:
        # Handle other errors
        return Response("An error occurred", status=500)

if __name__ == '__main__':
    app.run(debug=True)

