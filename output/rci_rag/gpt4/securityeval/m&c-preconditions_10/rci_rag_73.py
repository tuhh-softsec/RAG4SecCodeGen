from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, StreamingHttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied
from django.conf import settings
import os
from datetime import datetime
import re

# Ensure that the view only accepts GET requests
@require_http_methods(["GET"])
def getResource(request):
    '''
    Get username and date from the request, then
    send the file to the user by creating path by the username and date.
    '''
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to access this resource.")

    # Get username and date from the request
    username = request.GET.get('username')
    date_str = request.GET.get('date')

    # Validate the username and date
    if not username or not date_str:
        return HttpResponseBadRequest("Username and date parameters are required.")

    # Sanitize the username to prevent directory traversal or other injection attacks
    if not re.match(r'^[\w.@+-]+$', username) or '..' in username:
        return HttpResponseBadRequest("Invalid username.")

    # Check if the authenticated user is authorized to access the resource
    if username != request.user.username:
        return HttpResponseForbidden("You are not authorized to access this resource.")

    try:
        # Validate date format (e.g., YYYY-MM-DD)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return HttpResponseBadRequest("Invalid date format.")

    # Construct the file path
    file_path = os.path.join(settings.MEDIA_ROOT, username, date_str, 'resource.txt')

    # Resolve the real path to prevent directory traversal attacks
    real_file_path = os.path.realpath(file_path)
    if not real_file_path.startswith(os.path.realpath(settings.MEDIA_ROOT)):
        raise PermissionDenied("Access denied.")

    # Check if the file exists and is not a directory
    if not os.path.isfile(real_file_path):
        raise Http404("The requested resource does not exist.")

    # Stream the file content using a context manager to ensure the file is closed properly
    try:
        with open(real_file_path, 'rb') as file:
            response = StreamingHttpResponse(file, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(real_file_path)}"'
            response['X-Content-Type-Options'] = 'nosniff'  # Prevent MIME type sniffing

            # Additional security headers
            response['Content-Security-Policy'] = "default-src 'none';"
            response['X-Frame-Options'] = 'DENY'
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

            return response
    except IOError as e:
        # Log the error for further investigation
        # logger.error(f"Error streaming file {real_file_path}: {e}")
        raise Http404("The requested resource could not be opened.")

# Note: The settings SESSION_COOKIE_HTTPONLY, DEFAULT_CHARSET, and DEBUG should be configured in the Django project's settings file, not within the view code.

