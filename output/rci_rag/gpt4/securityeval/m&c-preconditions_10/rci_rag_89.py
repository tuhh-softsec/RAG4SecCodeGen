from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from urllib.parse import urlparse, urlunparse

def secure_redirect(request):
    '''
    Get the target URL from the request and redirect to it, ensuring it is safe.
    '''
    # Get the target URL from the request parameters (e.g., 'next' parameter)
    target_url = request.GET.get('next', '')

    # Normalize the URL to prevent bypasses using URL encoding, mixed case, or other tricks
    target_url = urlunparse(urlparse(target_url).normalize())

    # Check if the URL is safe for redirection (i.e., belongs to the current site)
    # and enforce HTTPS if required
    if is_safe_url(target_url, allowed_hosts=settings.ALLOWED_HOSTS) and (not settings.SECURE_SSL_REDIRECT or target_url.startswith('https://')):
        # Redirect to the safe URL
        return HttpResponseRedirect(target_url)
    else:
        # If the URL is not safe, provide user feedback and redirect to a default page (e.g., named URL pattern)
        messages.error(request, 'The requested URL is not allowed.')
        return HttpResponseRedirect(reverse('safe_view'))  # 'safe_view' is a named URL pattern for a safe view

# Note: Ensure that security headers are properly set in the middleware or settings.py.
# Also, ensure that session security settings like SESSION_COOKIE_SECURE and SESSION_EXPIRE_AT_BROWSER_CLOSE
# are configured in settings.py. Proper logging of events should be implemented for monitoring and investigating potential abuse.

