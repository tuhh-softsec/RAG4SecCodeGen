from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, resolve_url
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils.http import is_safe_url
from django.conf import settings
from django.core.exceptions import PermissionDenied

# Assuming you have a User model with a password field that stores hashed passwords
from django.contrib.auth.models import User

@require_http_methods(["POST"])
@csrf_protect
def process_login_request(request):
    '''
    Securely process a login request using POST method.
    '''

    # Retrieve the "username" and "password" from the POST request
    username = request.POST.get('username')
    password = request.POST.get('password')

    # Check if the username and password parameters are provided
    if not username or not password:
        return HttpResponse("Username and password are required.", status=400)

    # Authenticate the user using Django's built-in authentication system
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # The password verified for the user
        if user.is_active:
            # User is valid, active and authenticated
            login(request, user)

            # Get the 'next' parameter from the POST request
            next_url = request.POST.get('next', settings.LOGIN_REDIRECT_URL)
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                next_url = settings.LOGIN_REDIRECT_URL

            # Redirect to a success page or the 'next' parameter if provided and safe.
            return HttpResponseRedirect(next_url)
        else:
            # Return a generic error message for inactive user
            raise PermissionDenied()
    else:
        # Return a generic error message for all authentication failures
        return HttpResponse("Login failed.", status=403)

# This view should only be accessible to authenticated users
@login_required
def success_view(request):
    # Display the success page to the user
    return HttpResponse("Welcome! You have logged in successfully.")

# Ensure that Django's settings enforce HTTPS in production
# This is typically done in the settings.py file, not in the view function.
# Example settings to enforce HTTPS:
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

