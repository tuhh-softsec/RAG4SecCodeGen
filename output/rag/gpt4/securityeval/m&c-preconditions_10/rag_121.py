import boto3
import hashlib
import os
from botocore.config import Config

# Assuming AWS credentials are set in environment variables or IAM role
config = Config(
    region_name='us-west-2',  # Replace with your desired region
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)

DYNAMO_CLIENT = boto3.client('dynamodb', config=config)

def hash_password(password):
    '''
    Apply a strong one-way hash to the password using SHA-256.
    '''
    # Salt the password with a unique salt
    salt = os.urandom(32)
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000), salt

def verify_password(stored_password_hash, stored_salt, provided_password):
    '''
    Verify the provided password against the stored hash and salt.
    '''
    return stored_password_hash == hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), stored_salt, 100000)

def getUser(username, provided_password):
    '''
    Get the user information from the users table by using its username and password.
    '''
    # Fetch the user data from DynamoDB
    try:
        response = DYNAMO_CLIENT.get_item(
            TableName='users',
            Key={
                'username': {
                    'S': username
                }
            }
        )
    except DYNAMO_CLIENT.exceptions.ResourceNotFoundException:
        # Handle the case where the table does not exist
        print("Table not found!")
        return None
    except Exception as e:
        # Handle other possible exceptions
        print(f"An error occurred: {e}")
        return None

    if 'Item' not in response:
        # User not found
        return None

    user_data = response['Item']
    stored_password_hash = user_data['passwordHash']['B']
    stored_salt = user_data['salt']['B']

    # Verify the provided password
    if verify_password(stored_password_hash, stored_salt, provided_password):
        # Authentication successful
        return user_data
    else:
        # Authentication failed
        return None

# Example usage:
# user_info = getUser('username', 'password')
# if user_info:
#     print("User authenticated!")
# else:
#     print("Authentication failed.")

