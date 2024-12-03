from html_sanitizer import Sanitizer

def sanitize_html(content):
    '''
    Sanitize HTML content to remove potential XSS threats.
    '''
    # Configure the sanitizer with a whitelist of allowed tags and attributes
    sanitizer = Sanitizer({
        'tags': {'a', 'p', 'br', 'strong', 'em', 'div', 'span'},  # Add more as needed
        'attributes': {'href', 'title', 'style'},  # Add more as needed
        'empty': {'br'},  # Tags that can be empty
        'separate': {'a'},  # Tags that cannot be nested within themselves
        # Add more configuration as needed to ensure security
    })

    # Sanitize the HTML content
    cleaned_content = sanitizer.sanitize(content)
    
    return cleaned_content

# Example usage:
html_content = "<p>Hello World!</p><script>alert('This is a script!');</script><p>Goodbye!</p>"
filtered_content = sanitize_html(html_content)
print(filtered_content)

