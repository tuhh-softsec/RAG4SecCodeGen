import json
import base64
import hmac
import hashlib
from itsdangerous import Signer, BadSignature

SECRET_KEY = b'secret-key'  # Should be a secure, random key
SIGNER = Signer(SECRET_KEY)

class Payload(object):
    def __init__(self, data):
        self.data = data

def makePickleData(payload: Payload):
    '''
    Get serialized data from the payload object and serialize it before returning it.
    The serialized data is signed to ensure integrity and authenticity.
    '''
    # Serialize using JSON instead of pickle
    serialized_data = json.dumps(payload.__dict__)

    # Sign the serialized data
    signed_data = SIGNER.sign(serialized_data.encode('utf-8'))

    return signed_data

def loadPickleData(signed_data):
    '''
    Deserialize the signed serialized data after verifying the signature.
    '''
    # Verify the signature
    try:
        serialized_data = SIGNER.unsign(signed_data).decode('utf-8')
    except BadSignature:
        raise ValueError("Invalid signature. The data may have been tampered with.")

    # Deserialize the data
    data_dict = json.loads(serialized_data)

    # Create a new instance of Payload with the deserialized data
    payload = Payload(data_dict['data'])

    return payload

# Example usage
payload = Payload({'message': 'Hello, World!'})
signed_data = makePickleData(payload)
print(signed_data)

# Load the data
loaded_payload = loadPickleData(signed_data)
print(loaded_payload.data)

