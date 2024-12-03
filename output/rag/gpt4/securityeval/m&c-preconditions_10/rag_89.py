from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from urllib.parse import urlparse

# List of allowed hosts for redirection
ALLOWED_HOSTS = ['www.example.com', 'sub.example.com']

def http_responser_redirect(request):
    '''
    Get the target url from the request and redirect to it
    '''
    # Get the target URL from the request parameters (e.g., /redirect/?next=/page/)
    target_url = request.GET.get('next', '')

    # Parse the URL to retrieve the netloc (domain)
    parsed_url = urlparse(target_url)

    # Check if the URL's host is in the list of allowed hosts
    if parsed_url.netloc in ALLOWED_HOSTS and is_safe_url(target_url, allowed_hosts=ALLOWED_HOSTS):
        # Redirect to the safe target URL
        return HttpResponseRedirect(target_url)
    else:
        # Redirect to a default page if the URL is not safe
        return HttpResponseRedirect('/')

# Ensure that the session cookie is set to HttpOnly
# This is typically done in Django settings, not in the view itself
SESSION_COOKIE_HTTPONLY = True

# Specify encoding in the HTTP header
# This is typically done in Django settings, not in the view itself
DEFAULT_CHARSET = 'utf-8'

# Ensure that Django is run with debugging disabled
# This is typically done in Django settings, not in the view itself
DEBUG = False

