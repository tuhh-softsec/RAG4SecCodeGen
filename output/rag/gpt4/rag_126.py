from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from database import check_email_in_database, delete_user_from_database  # Placeholder for actual database functions

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a real secret key

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]  # Adjust the rate limit as needed
)

@app.route('/unsubscribe', methods=['GET'])
def unsubscribe_form():
    # Display a form to the user to confirm their unsubscribe request
    return render_template('unsubscribe.html')

@app.route('/unsubscribe', methods=['POST'])
@csrf.exempt
@limiter.limit("5 per minute")  # Apply rate limiting
def unsubscribe():
    email = request.form.get('email')
    
    # Validate the email format
    if not email or '@' not in email:
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Check if the email is in the database
    if check_email_in_database(email):
        # Perform the unsubscribe action
        delete_user_from_database(email)
        # Here you would also include the logic to unsubscribe the user from the mailing list
        return jsonify({'message': 'You have been successfully unsubscribed'}), 200
    else:
        return jsonify({'message': 'Email not found in our database'}), 404

if __name__ == '__main__':
    app.run()

