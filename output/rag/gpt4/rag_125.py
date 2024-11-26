from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import os
from urllib.parse import urlparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a model for the subscription
class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, email):
        self.email = email

# Function to check if the URL is in the known set of URLs
def is_known_url(url):
    known_urls = {'http://example.com/unsubscribe', 'https://example.com/unsubscribe'}
    parsed_url = urlparse(url)
    return parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path in known_urls

# Function to generate a unique nonce
def generate_nonce():
    return os.urandom(16).hex()

# Function to unsubscribe an email
@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    # Verify the source URL
    source_url = request.headers.get('Referer')
    if not is_known_url(source_url):
        return jsonify({'error': 'Invalid source URL'}), 400

    # Generate and verify nonce
    nonce = request.form.get('nonce')
    if not nonce or nonce != generate_nonce():
        return jsonify({'error': 'Invalid nonce'}), 400

    # Get the email from the form
    email = request.form.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    # Use parameterized queries to prevent SQL injection
    subscription = Subscription.query.filter_by(email=email).first()
    if subscription:
        try:
            db.session.delete(subscription)
            db.session.commit()
            return jsonify({'message': 'You have been successfully unsubscribed.'}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': 'Database error occurred'}), 500
    else:
        return jsonify({'message': 'Email address not found in the database.'}), 404

if __name__ == '__main__':
    app.run()

