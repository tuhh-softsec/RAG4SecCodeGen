import re

def contains_digit(input_string, ascii_only=False):
    """
    Check if the input string contains any decimal digits.

    Args:
        input_string (str): The string to be checked for digits.
        ascii_only (bool): If True, only ASCII digits will be matched.

    Returns:
        bool: True if the string contains at least one digit, False otherwise.

    Raises:
        TypeError: If the input is not a string.

    Note:
        The function uses a simple regular expression and is not susceptible to
        ReDoS attacks. It matches Unicode digits by default, which can be
        restricted to ASCII by setting ascii_only to True.
    """
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    # Regular expression pattern to find digits
    pattern = re.compile(r'[0-9]' if ascii_only else r'\d')  # \d matches any Unicode decimal digit
    
    # Search the string for any matches to the pattern
    return bool(pattern.search(input_string))

# Example usage:
try:
    number_string = "This is a test string with number 12345"
    print(contains_digit(number_string))  # Output: True

    non_number_string = "This string has no numbers"
    print(contains_digit(non_number_string))  # Output: False

    invalid_input = 12345  # Not a string
    print(contains_digit(invalid_input))  # Raises TypeError
except TypeError as e:
    print(f"Error: {e}")
except Exception as e:
    # Handle other potential exceptions gracefully
    print(f"An unexpected error occurred: {e}")

