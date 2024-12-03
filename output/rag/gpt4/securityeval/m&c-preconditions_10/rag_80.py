from django.conf.urls import url
from django.http import HttpResponseBadRequest, JsonResponse
import json
import hmac
import hashlib
import base64

# Secret key for HMAC
SECRET_KEY = b'my-secret-key'

# List of classes you are willing to deserialize
ALLOWED_CLASSES = ['MySafeClass']

def is_safe_class(obj):
    """
    Check if the object is an instance of allowed classes.
    """
    if obj.__class__.__name__ in ALLOWED_CLASSES:
        return True
    return False

def verify_hmac(pickled_data, signature):
    """
    Verify the HMAC signature of the data.
    """
    hmac_obj = hmac.new(SECRET_KEY, pickled_data, hashlib.sha256)
    expected_signature = base64.b64encode(hmac_obj.digest()).decode()
    return hmac.compare_digest(expected_signature, signature)

def getPickleData(request):
    """
    Return deserialized data if it's safe and the signature is verified.
    """
    try:
        # Assuming the pickled data and signature are sent in the request body as JSON
        body = json.loads(request.body)
        pickled_data = body.get('data')
        signature = body.get('signature')

        # Verify the integrity of the serialized data
        if not verify_hmac(pickled_data.encode(), signature):
            return HttpResponseBadRequest('Invalid data signature')

        # Deserialize the data safely
        data = pickle.loads(base64.b64decode(pickled_data), fix_imports=True)

        # Validate the deserialized data
        if not is_safe_class(data):
            return HttpResponseBadRequest('Unsafe deserialization attempt')

        # Process the deserialized data
        # ...

        return JsonResponse({'status': 'success', 'data': 'Processed successfully'})

    except Exception as e:
        # Handle exceptions
        return HttpResponseBadRequest(f'An error occurred: {str(e)}')

# URL configuration
urlpatterns = [
    url(r'^get_pickle_data/$', getPickleData),
]

# Remember to disable debugging in production
DEBUG = False

