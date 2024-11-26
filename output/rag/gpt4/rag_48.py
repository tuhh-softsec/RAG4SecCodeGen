import html

# Assuming a web framework that provides request and response objects
def http_hello_page(request, response):
    # Guideline #4: Apply authentication before returning the requested page
    if not user_is_authenticated(request):
        response.status_code = 401  # Unauthorized
        response.write("Unauthorized access")
        response.close()
        return

    # Guideline #1: Do not reflect data directly from the HTTP request
    # Read the username safely, assuming the framework provides a method to read the request body
    username = request.get_body().decode('utf-8')
    
    # Guideline #3: Use a stringent allowlist for the username
    # For example, only allow alphanumeric characters for the username
    if not username.isalnum():
        response.status_code = 400  # Bad Request
        response.write("Invalid username")
        response.close()
        return

    # Guideline #5: Appropriately encode all non-alphanumeric characters
    # Encode the username to prevent XSS attacks
    safe_username = html.escape(username)

    # Construct the response body with the safe username
    outputbuf = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Hello Page</title>
        <!-- Guideline #2: Specify encoding in the HTTP header -->
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </head>
    <body>
        <h1>Hello, {safe_username}!</h1>
    </body>
    </html>
    """

    # Write the response body to the response stream
    response.status_code = 200  # OK
    response.write(outputbuf)

    # Close the response stream
    response.close()

    # The server is now ready to handle the next request

# Helper function to check if the user is authenticated
def user_is_authenticated(request):
    # Implement authentication logic here
    # For example, check for session cookies or authentication headers
    return True  # Placeholder for actual authentication check

# Assuming the web framework calls this function when the server starts
def main():
    # Register the URL and the function that handles it
    register_url_handler('/hello', http_hello_page)

    # Start the server
    start_server()

if __name__ == "__main__":
    main()

