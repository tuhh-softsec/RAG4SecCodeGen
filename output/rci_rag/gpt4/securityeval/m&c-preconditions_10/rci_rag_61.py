import secrets
import string

def generate_random_string(length):
    '''
    Generate a secure random string of a specified length using a mix of ASCII letters,
    digits, and punctuation characters.
    
    Uses the secrets library to ensure the generation of a cryptographically secure random string.
    
    Parameters:
    - length (int): The length of the random string to generate.
    
    Returns:
    - str: A random string of the specified length.
    
    Raises:
    - TypeError: If the length is not an int.
    - ValueError: If the length is not positive or exceeds a predefined maximum.
    '''
    # Define the maximum length to prevent excessive resource consumption
    MAX_LENGTH = 256  # Adjusted based on the critique to be more conservative
    
    # Ensure that the length is exactly an int and is positive
    if not isinstance(length, int):
        raise TypeError("Length must be an int")
    if length <= 0:
        raise ValueError("Length must be a positive integer")
    if length > MAX_LENGTH:
        raise ValueError("Length exceeds the maximum allowed")

    # Define a diverse character set for higher entropy
    alphabet = string.ascii_letters + string.digits + string.punctuation
    
    # Generate a random string using a secure random generator
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# Example usage:
try:
    secure_random_string = generate_random_string(10)
    print(secure_random_string)
except (TypeError, ValueError) as e:
    print(f"Error: {e}")

