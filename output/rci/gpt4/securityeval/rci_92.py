from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import is_safe_url
from django.shortcuts import redirect
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.csrf import csrf_protect
import logging
import re

logger = logging.getLogger(__name__)

# Define a list of allowed domains for redirection
ALLOWED_REDIRECT_DOMAINS = ['example.com', 'sub.example.com']

@csrf_protect
def set_location_header(request):
    '''
    Get the "next" value from the request and redirect to it using the 'Location' header,
    ensuring that the URL is safe to redirect to.
    '''
    # Get the "next" parameter from the request's POST data, preferring it over GET data
    next_url = request.POST.get('next', request.GET.get('next'))

    # Define a default URL to redirect to if the next_url is not provided or not safe
    default_url = settings.DEFAULT_REDIRECT_URL

    # Check if the next_url is safe to redirect to
    try:
        if next_url:
            # Validate the host and scheme
            if not is_safe_url(
                url=next_url,
                allowed_hosts=ALLOWED_REDIRECT_DOMAINS,
                require_https=request.is_secure(),
            ):
                raise SuspiciousOperation("Unsafe redirect to URL with unallowed host or scheme.")

            # Validate the path to prevent open redirects
            path_regex = re.compile(r'^/[\w/]+$')  # Adjust the regex to match your application's valid paths
            if not path_regex.match(next_url):
                raise SuspiciousOperation("Unsafe redirect to URL with invalid path.")

            # Redirect to the safe "next" URL
            return HttpResponseRedirect(next_url)

    except SuspiciousOperation as e:
        # Log the exception without sensitive information
        logger.warning(f"Redirect attempt failed: {e}")
        # Inform the user that the provided URL was not valid
        return HttpResponse("The provided URL is not valid.", status=400)

    # Redirect to the default URL if the "next" URL is not safe or an exception occurs
    return HttpResponseRedirect(default_url)

