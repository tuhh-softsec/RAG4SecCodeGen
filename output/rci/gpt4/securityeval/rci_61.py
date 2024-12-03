import secrets
import string

def generate_secure_random_string(min_length=12, max_length=24, allowed_chars=None):
    '''
    Generate a cryptographically secure random string with a variable length.
    
    The string includes ASCII letters, digits, and punctuation by default, and its length
    is randomly chosen between min_length and max_length to add unpredictability.
    
    Parameters:
    - min_length (int): The minimum length of the random string (default is 12).
    - max_length (int): The maximum length of the random string (default is 24).
    - allowed_chars (str): A string of characters that are allowed in the random string.
    
    Returns:
    - str: A secure random string.
    
    Raises:
    - ValueError: If min_length or max_length is not a positive integer, or if min_length > max_length.
    '''
    
    # Validate input parameters
    if not (isinstance(min_length, int) and isinstance(max_length, int)):
        raise ValueError("min_length and max_length must be integers.")
    if min_length <= 0 or max_length <= 0:
        raise ValueError("min_length and max_length must be positive.")
    if min_length > max_length:
        raise ValueError("min_length must not be greater than max_length.")
    if max_length > 1024:  # Set a reasonable upper limit to prevent DoS attacks
        raise ValueError("max_length is too large. Please choose a smaller value.")

    # Define the characters that can be used in the string
    characters = allowed_chars if allowed_chars is not None else string.ascii_letters + string.digits + string.punctuation
    
    # Randomly choose the length of the string for added unpredictability
    length = secrets.randbelow(max_length - min_length + 1) + min_length
    
    # Use secrets.choice to generate a random string
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    
    return random_string

# Example usage:
try:
    print(generate_secure_random_string())
except ValueError as e:
    print(f"Error: {e}")

