from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import redirect
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def secure_redirect(request):
    '''
    Get the target URL from the request and redirect to it securely.
    '''
    # Define a dedicated list of allowed redirect hosts
    allowed_redirect_hosts = getattr(settings, 'ALLOWED_REDIRECT_HOSTS', [])

    # Get the target URL from the request, e.g., using GET parameter 'next'
    target_url = request.GET.get('next', '')

    # Validate and sanitize the target URL
    if not target_url:
        # Log the missing 'next' parameter
        logger.warning("Missing 'next' parameter for redirect.")
        return redirect('default_page_name')  # Replace 'default_page_name' with the name of your default route

    # Explicitly control HTTPS requirements for redirects with a dedicated setting
    require_https = getattr(settings, 'SECURE_REDIRECTS', not settings.DEBUG)

    # Check if the host of the target URL is safe to redirect to
    try:
        if url_has_allowed_host_and_scheme(url=target_url, allowed_hosts=allowed_redirect_hosts, require_https=require_https):
            # Perform additional validation on the path and query parameters
            # (This step may involve custom validation logic specific to your application's needs)
            # ...

            # Redirect to the safe target URL
            return HttpResponseRedirect(target_url)
        else:
            # Log the failed redirect attempt without sensitive information
            logger.warning(f"Unsafe redirect attempt blocked.")
            # Redirect to a default page if the target URL is not safe
            return redirect('default_page_name')  # Replace 'default_page_name' with the name of your default route
    except Exception as e:  # Catch all exceptions to handle unexpected errors
        # Log the exception without sensitive information
        logger.error(f"Error processing redirect: {type(e).__name__}")
        # Return a bad request response or redirect to a default page
        return HttpResponseBadRequest("Invalid redirect URL.")

# Note: Replace 'default_page_name' with the actual name of a safe route in your application.

