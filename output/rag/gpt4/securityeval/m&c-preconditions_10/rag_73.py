import os
from django.http import HttpResponse, HttpResponseForbidden, FileResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import SuspiciousOperation
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.decorators import login_required
from urllib.parse import urlparse

# Ensure that the Django application is not running in debug mode in production
# This should be set in the settings.py file
# DEBUG = False

@login_required
@require_http_methods(["GET"])
def getResource(request):
    '''
    Get username and date from the request, then
    send the file to the user by creating path by the username and date.
    '''
    # Ensure the session cookie is set to HttpOnly
    request.session.set_expiry(0)  # Session expires when the browser is closed
    request.session.modified = True

    # Validate the data in the request
    username = request.GET.get('username')
    date = request.GET.get('date')

    # Use allowlist to validate the username and date format
    if not username.isalnum():
        raise SuspiciousOperation("Invalid username")
    
    # Here you should also validate the date format strictly
    # For example, using regex or a date parsing function that strictly adheres to a format

    # Check if the user is authorized to access the file
    if username != request.user.username:
        return HttpResponseForbidden("You are not authorized to access this file.")

    # Construct the file path securely
    base_dir = '/path/to/secure/storage'
    file_path = os.path.join(base_dir, username, date)

    # Prevent directory traversal attacks
    if not os.path.normpath(file_path).startswith(base_dir):
        raise SuspiciousOperation("Invalid file path")

    # Check if the file exists
    if not os.path.isfile(file_path):
        return HttpResponseNotFound("File not found.")

    # Set the content type and encoding in the HTTP header
    response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    response['Content-Encoding'] = 'utf-8'

    return response

# Additional security settings can be enforced in Django settings.py, such as:
# CSRF_COOKIE_HTTPONLY = True
# SESSION_COOKIE_HTTPONLY = True
# SECURE_BROWSER_XSS_FILTER = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_CONTENT_TYPE_NOSNIFF = True

