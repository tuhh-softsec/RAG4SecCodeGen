from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import is_safe_url
from django.conf import settings
from urllib.parse import urlparse

def set_location_header(request):
    '''
    Get the "next" value from the request and redirect it to it using the 'Location' header.
    '''
    # Get the "next" parameter from the request
    next_url = request.GET.get('next', '')

    # Validate the "next" URL
    if not is_safe_url(url=next_url, allowed_hosts=settings.ALLOWED_HOSTS):
        # If the URL is not safe, redirect to a default page or reject the request
        return HttpResponse("Invalid 'next' parameter", status=400)

    # Ensure the user is authorized to access the next_url (implement your authorization logic here)
    # if not user_is_authorized(request.user, next_url):
    #     return HttpResponse("Unauthorized", status=403)

    # Create a response object and set the 'Location' header to the safe URL
    response = HttpResponse(status=302)
    response['Location'] = next_url

    # Set the session cookie to HttpOnly
    response.set_cookie('sessionid', request.COOKIES.get('sessionid'), httponly=True)

    # Specify encoding in the HTTP header
    response['Content-Type'] = 'text/html; charset=utf-8'

    return response

# Note: The user_is_authorized function is a placeholder for your actual authorization logic.
# You should implement this function to check if the user has the right to access the next_url.

