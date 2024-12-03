import bleach
from bleach.sanitizer import Cleaner

# Define a cleaner with a specific whitelist of allowed tags, attributes, and styles
# Customize this whitelist according to the needs of your application and ensure it's safe
allowed_tags = ['p', 'strong', 'em']
allowed_attributes = {'a': ['href', 'title']}
allowed_styles = []

cleaner = Cleaner(tags=allowed_tags, attributes=allowed_attributes, styles=allowed_styles, strip=True)

def filterScriptTags(content):
    '''
    Remove <script> tags and other potentially malicious content from the content argument.
    This function uses the bleach library to sanitize the content, which is more secure
    than using regex. It also considers additional security practices.
    '''
    try:
        # Use the predefined cleaner to sanitize the content
        sanitized_content = cleaner.clean(content)
    except Exception as e:
        # Handle any exceptions that occur during sanitization
        # Log the error and/or take appropriate action
        sanitized_content = ''
        # Depending on your application, you might want to log the error, notify an admin, etc.
        print(f"Error sanitizing content: {e}")

    return sanitized_content

# Example usage:
content_with_scripts = '<p>Hello World!</p><script>alert("XSS")</script>'
clean_content = filterScriptTags(content_with_scripts)
print(clean_content)

