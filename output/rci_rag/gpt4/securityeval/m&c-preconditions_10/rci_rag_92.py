from django.http import HttpResponseRedirect
from django.core.exceptions import SuspiciousOperation
from django.utils.http import is_safe_url
from django.conf import settings

def redirect_to_next(request):
    '''
    Get the "next" value from the request and redirect to it.
    '''
    # Get the "next" parameter from the request or default to a safe home URL
    next_url = request.GET.get('next', '/')

    # Ensure the URL is safe to redirect to
    if not is_safe_url(url=next_url, allowed_hosts=settings.ALLOWED_HOSTS, require_https=request.is_secure()):
        raise SuspiciousOperation('Unsafe redirect to URL: {}'.format(next_url))

    # Ensure the user is authorized to access the URL
    if not user_is_authorized(request.user, next_url):
        return HttpResponse('Unauthorized', status=401)

    # Use HttpResponseRedirect to handle redirection
    response = HttpResponseRedirect(next_url)

    # Do not set the CSRF token in the response header for a redirect
    # Do not manually set the sessionid cookie; rely on Django's session management

    return response

def user_is_authorized(user, url):
    # Placeholder function for checking user authorization
    # Implement your authorization logic here
    return True  # Assume the user is authorized for the purpose of this example

# Ensure that the Django application is run with debugging disabled
# This is typically set in the Django settings file, not within the view function
# settings.py
# DEBUG = False

# Additional improvements:
# - Implement proper error handling and logging
# - Ensure that the application is configured to recognize HTTPS behind a proxy
# - Enforce CSRF protection for all POST requests

