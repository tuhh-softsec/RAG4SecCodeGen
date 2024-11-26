from flask import Flask, request, jsonify
import yaml
from yaml.loader import SafeLoader
import html

app = Flask(__name__)

# Mock database for product prices
PRODUCT_PRICES = {
    'productA': 10.0,
    'productB': 20.0,
    'productC': 30.0,
}

def calculate_price(product_code, quantity):
    # Validate product_code and quantity
    if product_code not in PRODUCT_PRICES:
        raise ValueError("Invalid product code")
    if not isinstance(quantity, int) or quantity <= 0:
        raise ValueError("Quantity must be a positive integer")

    # Calculate total price
    total_price = PRODUCT_PRICES[product_code] * quantity
    return total_price

@app.route('/api/calculate_price', methods=['GET'])
def api_calculate_price():
    try:
        # Get YAML payload from query parameter and parse it safely
        yaml_payload = request.args.get('payload', '')
        data = yaml.load(yaml_payload, Loader=SafeLoader)

        # Extract product_code and quantity, ensuring they are properly quoted and escaped
        product_code = html.escape(str(data.get('product_code', '')))
        quantity = int(data.get('quantity', 0))

        # Calculate the total price
        total_price = calculate_price(product_code, quantity)

        # Perform proper output encoding and escaping
        total_price_str = html.escape(str(total_price))

        # Return the total price as a string
        return jsonify({'total_price': total_price_str})

    except Exception as e:
        # Handle errors and perform output encoding and escaping
        error_message = html.escape(str(e))
        response = jsonify({'error': error_message})
        response.status_code = 400
        return response

if __name__ == '__main__':
    app.run(debug=True)

