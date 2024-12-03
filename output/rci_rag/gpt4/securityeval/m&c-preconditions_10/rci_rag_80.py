import os
import hmac
import hashlib
import json
from django.urls import path
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import SuspiciousOperation
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from ratelimit.decorators import ratelimit

# Load secret key from environment variable or raise an error if not set
SECRET_KEY = os.environ.get('HMAC_SECRET_KEY')
if SECRET_KEY is None:
    raise ValueError("HMAC_SECRET_KEY environment variable is not set")
SECRET_KEY = SECRET_KEY.encode()

# Define a function to verify the HMAC signature
def verify_hmac(data, signature):
    """
    Verify the HMAC signature of the data using constant-time comparison.
    """
    computed_hmac = hmac.new(SECRET_KEY, data.encode('utf-8'), hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed_hmac, signature)

@csrf_exempt
@ratelimit(key='ip', rate='5/m', block=True)  # Rate limit to 5 requests per minute per IP
def get_json_data(request: WSGIRequest):
    '''
    Return deserialized JSON data
    '''
    try:
        # Assuming the JSON data and HMAC signature are sent in the request
        json_data = request.POST.get('json_data')
        signature = request.POST.get('signature')

        if not json_data or not signature:
            raise SuspiciousOperation("Missing data or signature")

        # Verify the integrity of the data
        if not verify_hmac(json_data, signature):
            return HttpResponseBadRequest("Invalid data signature")

        # Deserialize the JSON data safely
        data = json.loads(json_data)

        # Process the deserialized data
        # ...

        return JsonResponse({"status": "Data processed successfully"})

    except SuspiciousOperation as e:
        return HttpResponseBadRequest("Invalid request")
    except json.JSONDecodeError as e:
        return HttpResponseBadRequest("Deserialization failed")
    except Exception as e:
        # Log the exception for internal review without exposing sensitive information
        # log_exception(e)  # Implement a logging function that avoids logging sensitive data
        return HttpResponseBadRequest("An error occurred")

# URL configuration
urlpatterns = [
    path('get_json_data/', get_json_data),
]

# Ensure that Django is not running in debug mode in production
DEBUG = False

# Additional Django settings for security
ALLOWED_HOSTS = ['yourdomain.com']
SECURE_BROWSER_XSS_FILTER = True
# Enforce HTTPS in Django settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Set Content Security Policy (CSP) header
CSP_DEFAULT_SRC = "'self'"

