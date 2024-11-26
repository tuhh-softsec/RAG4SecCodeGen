from flask import Flask, request, session, redirect, url_for, render_template_string, abort
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a real secret key

# In-memory 'database' for demonstration purposes
# In a real application, you would use a proper database system
products = {
    '001': 19.99,
    '002': 29.99,
    '003': 39.99
}

# In-memory user storage
users = {
    'admin': generate_password_hash('password')  # Replace with real user data and secure passwords
}

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['user_id'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password', 401
    return '''
        <form method="post">
            Username: <input type="text" name="username">
            Password: <input type="password" name="password">
            <input type="submit" value="Login">
        </form>
    '''

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# Function to get the price of a product
def get_price(product_code):
    return products.get(product_code, 0)

# Route to calculate the price
@app.route('/calculate_price', methods=['POST'])
@login_required
def calculate_price():
    product_code = request.form['product_code']
    quantity = int(request.form['quantity'])
    
    # Ensure that the product code and quantity are safe to use
    if not product_code.isalnum() or quantity < 0:
        abort(400)  # Bad request
    
    price = get_price(product_code)
    total_price = price * quantity
    
    # Render a safe template without user-supplied data
    return render_template_string('''
        <h1>Price Calculation</h1>
        <p>Product Code: {{ product_code }}</p>
        <p>Quantity: {{ quantity }}</p>
        <p>Total Price: {{ total_price }}</p>
        <a href="{{ url_for('logout') }}">Logout</a>
    ''', product_code=product_code, quantity=quantity, total_price=total_price)

# Index route
@app.route('/')
@login_required
def index():
    return 'Welcome to the secure web app!'

if __name__ == '__main__':
    app.run(port=5000)

