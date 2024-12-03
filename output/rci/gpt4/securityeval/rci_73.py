import os
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.conf import settings
from datetime import datetime
import logging

@login_required
def getResource(request):
    '''
    Get username and date from the request, then
    send the file to the user by creating path by the username and date.
    Ensure that the user is authenticated and authorized to access the file.
    Validate the input to prevent path traversal attacks.
    '''
    # Get username and date from the request
    username = request.user.username  # Assuming the user is authenticated
    date = request.GET.get('date', '')  # Get the date from the query parameters

    # Validate the date format to prevent path traversal or other attacks
    try:
        # Use a strict date parsing method to validate the date format
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        logging.warning(f"Invalid date format access attempt by user {username}")
        raise Http404("Invalid date format")

    # Construct the file path using safe methods
    base_dir = getattr(settings, 'USER_FILES_DIR', '/path/to/user/files/')
    if base_dir.endswith('/'):
        base_dir = base_dir[:-1]  # Ensure base_dir does not end with a slash

    # Implement actual authorization logic
    if not is_user_authorized_to_access_file(username, date):
        logging.warning(f"Unauthorized file access attempt by user {username}")
        raise PermissionDenied("You do not have permission to access this file.")

    file_path = os.path.join(base_dir, username, date, 'yourfile.txt')

    # Resolve any symbolic links
    real_base_dir = os.path.realpath(base_dir)
    real_file_path = os.path.realpath(file_path)

    # Check if the file exists and is within the allowed path
    if not os.path.exists(real_file_path) or not os.path.isfile(real_file_path):
        logging.error(f"File not found: {real_file_path}")
        raise Http404("File does not exist")

    # Check if the file path is within the base_dir to prevent path traversal
    if not real_file_path.startswith(real_base_dir):
        logging.error(f"Path traversal attempt: {real_file_path}")
        raise SuspiciousOperation("Invalid file path")

    # Serve the file using FileResponse for efficient streaming
    with open(real_file_path, 'rb') as file:
        response = FileResponse(file, as_attachment=True)
        response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(real_file_path)
        response['X-Content-Type-Options'] = 'nosniff'
        # Additional security headers can be added here
        response['Content-Security-Policy'] = "default-src 'none';"
        response['X-Frame-Options'] = 'DENY'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    return response

def is_user_authorized_to_access_file(username, date):
    # Implement actual checks based on your application's requirements
    # This should check the user's permissions and whether they are allowed to access the file for the given date
    # For example:
    # return user_has_permission(username, 'read', date)
    raise NotImplementedError("Authorization logic needs to be implemented")

# Additional helper functions can be defined here, such as user_has_permission

