import secrets
import string

def generate_secure_random_string(length):
    '''
    Return an unpredictable random string that has only ASCII letters with a fixed size equals to length.
    Preconditions: The code unit generates random numbers.
    Guidelines: Use a secure random generator with Python standard secrets library.
    '''
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Length must be a positive integer")

    # Guideline #3: Limit the length of strings or character arrays
    max_length = 1024  # Define a reasonable max length for the string
    if length > max_length:
        raise ValueError(f"Length must not exceed {max_length}")

    # Generate the random string using the secrets module for cryptographic security
    alphabet = string.ascii_letters
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# Example usage:
secure_random_string = generate_secure_random_string(10)
print(secure_random_string)

