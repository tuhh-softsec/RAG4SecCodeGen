from flask import request, Response, Flask, redirect, url_for, make_response
from urllib.parse import urlparse, urljoin
from flask import abort

app = Flask(__name__)
app.config['DEBUG'] = False  # Guideline #10: Ensure Flask app is run with debugging disabled

# Helper function to check if the URL is safe for redirects
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@app.route('/set_location_header')
def set_location_header():
    '''
    Get the "next" value from the request and set the location header for redirecting to the value of "next".
    '''
    next_url = request.args.get('next', '')  # Guideline #4: Validate the data in the request
    if not next_url or not is_safe_url(next_url):  # Guideline #7: Do not accept untrusted data
        abort(400)  # Bad request if the next URL is not provided or is not safe

    response = make_response(redirect(next_url))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'  # Guideline #3: Specify encoding in the HTTP header
    response.headers['X-Content-Type-Options'] = 'nosniff'  # Prevent MIME type sniffing
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'  # Clickjacking protection
    response.headers['X-XSS-Protection'] = '1; mode=block'  # XSS protection
    response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'  # Referrer policy
    response.headers['Content-Security-Policy'] = "default-src 'self'"  # CSP header
    response.set_cookie('session', 'value', httponly=True, secure=True)  # Guideline #2: Set session cookie to HttpOnly and secure

    # Additional security checks and configurations can be added here as needed

    return response

if __name__ == '__main__':
    app.run()

