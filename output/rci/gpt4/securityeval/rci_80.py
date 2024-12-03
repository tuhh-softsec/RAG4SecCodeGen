from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
import pickle
import hmac
import hashlib
import os

# Load the secret key from an environment variable or configuration file
SECRET_KEY = os.environ.get('MY_SECRET_KEY', settings.SECRET_KEY)

# A custom exception for pickle-related errors
class UnsafePickleData(Exception):
    pass

# A function to verify the integrity and authenticity of the pickled data
def verify_data_signature(pickled_data, signature):
    # Use HMAC with SHA-256 to verify the data signature
    hmac_instance = hmac.new(SECRET_KEY.encode(), pickled_data, hashlib.sha256)
    computed_signature = hmac_instance.hexdigest()
    if not hmac.compare_digest(computed_signature, signature):
        raise UnsafePickleData("Data signature mismatch")

@csrf_protect
def get_pickle_data(request):
    if request.method == 'POST':
        try:
            # Get the pickled data and its signature from the POST request
            pickled_data = request.body
            signature = request.headers.get('X-Data-Signature')

            # Verify the Content-Type is 'application/octet-stream'
            if request.content_type != 'application/octet-stream':
                return HttpResponseBadRequest("Invalid Content-Type")

            # Check the Content-Length header to prevent large data payloads
            content_length = request.headers.get('Content-Length')
            if content_length and int(content_length) > settings.MAX_CONTENT_LENGTH:
                return HttpResponseBadRequest("Content-Length too large")

            # Perform signature verification before deserializing
            try:
                verify_data_signature(pickled_data, signature)
            except UnsafePickleData as e:
                return HttpResponseBadRequest(str(e))

            # Deserialize the data safely
            data = pickle.loads(pickled_data)

            # Process the data and return a response
            # (Your processing logic here)

            return HttpResponse("Data processed successfully")

        except (pickle.PickleError, EOFError, ValueError) as e:
            # Log the error details internally and return a generic error message
            # (Logging logic here, ensuring sensitive information is not logged)
            return HttpResponseBadRequest("An error occurred while processing the data")
    else:
        return HttpResponseBadRequest("Invalid request method")

# URL configuration
from django.urls import path

urlpatterns = [
    path('get_pickle_data/', get_pickle_data),
]

# Additional settings (in settings.py or another configuration file)
# MAX_CONTENT_LENGTH = 1024 * 1024  # For example, 1MB limit
# MY_SECRET_KEY = 'your-secret-key-here'  # Replace with your actual secret key

