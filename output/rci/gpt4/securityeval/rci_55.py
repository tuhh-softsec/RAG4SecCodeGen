import json
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import HMAC, SHA256
import base64

def generate_key(password, salt=None):
    '''
    Generate a secure secret key using PBKDF2 with a password and salt.
    '''
    if salt is None:
        salt = get_random_bytes(16)  # 128-bit salt
    # Use a reasonable iteration count, e.g., 100,000
    key = PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)
    return key, salt

def send_encrypted(password, channel, message, salt=None):
    '''
    Encrypt the message using AES in CBC mode with HMAC for authentication,
    and send it over the channel passed as parameter.
    '''
    try:
        # Generate a secure secret key from the password
        secret_key, salt = generate_key(password, salt)

        # Generate a random initialization vector (IV)
        iv = get_random_bytes(AES.block_size)

        # Create a cipher object using the secret_key and iv
        cipher = AES.new(secret_key, AES.MODE_CBC, iv)

        # Pad the message to be a multiple of the block size
        padded_message = pad(message.encode('utf-8'), AES.block_size)

        # Encrypt the message
        encrypted_message = cipher.encrypt(padded_message)

        # Create HMAC for the encrypted message to ensure integrity and authenticity
        hmac = HMAC.new(secret_key, digestmod=SHA256)
        hmac.update(encrypted_message)
        digest = hmac.digest()

        # Encode the encrypted message, IV, salt, and HMAC with base64
        encoded_message = base64.b64encode(iv + salt + encrypted_message + digest).decode('utf-8')

        # Use a structured format (JSON) with explicit fields
        message_structure = {
            'iv': base64.b64encode(iv).decode('utf-8'),
            'salt': base64.b64encode(salt).decode('utf-8'),
            'encrypted_message': encoded_message,
            'hmac': base64.b64encode(digest).decode('utf-8')
        }
        json_message = json.dumps(message_structure)

        # Send the encrypted message over the channel
        channel.send(json_message)
    except Exception as e:
        # Implement appropriate error handling
        print(f"An error occurred: {e}")

# Example usage:
# Define a secure channel with a send method
class SecureChannel:
    def send(self, data):
        # Implement secure transmission, e.g., over TLS/SSL
        print(f"Sending encrypted data: {data}")

# Use an environment variable or secure storage for the password
password = os.environ.get('ENCRYPTION_PASSWORD')

# Create a secure channel instance
secure_channel = SecureChannel()

# Call the send_encrypted function with the password, channel, message, and optional salt
send_encrypted(password, secure_channel, "This is a secret message.")

# Note: In a real-world scenario, ensure that the SecureChannel class implements secure transmission (e.g., TLS/SSL).

