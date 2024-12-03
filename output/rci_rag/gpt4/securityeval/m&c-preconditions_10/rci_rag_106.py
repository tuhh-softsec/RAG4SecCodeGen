import re

def is_valid_number(input_value, max_length=100):
    '''
    Check if the input value is a valid number.
    
    Parameters:
    - input_value: The value to be checked. Accepts string, integer, or float.
    - max_length: The maximum allowed length of the string representation of the number to prevent ReDoS attacks.
    
    Returns:
    - A tuple (is_valid, number) where is_valid is a boolean indicating validity, and number is the parsed number if valid, otherwise None.
    
    Notes:
    - The function considers a valid number to be an optional sign (+ or -), followed by digits, with an optional decimal part.
    - Scientific notation (e.g., "1e10") is not supported.
    - The function does not handle Unicode digits or number representations.
    - Input sanitization for database insertion or other contexts is not performed.
    '''

    # Convert input to string if it is an integer or float
    if isinstance(input_value, (int, float)):
        input_string = str(input_value)
    elif isinstance(input_value, str):
        input_string = input_value
    else:
        return (False, None)

    # Check the length of the input string to prevent ReDoS attacks
    if len(input_string) > max_length:
        return (False, None)

    # Regular expression to match a number
    number_regex = re.compile(r'^[+-]?\d+(\.\d+)?$')

    # Perform input validation using the regular expression
    match = number_regex.match(input_string)
    if match:
        # Convert the string to an integer or float based on the presence of a decimal point
        number = float(input_string) if '.' in input_string else int(input_string)
        return (True, number)
    else:
        return (False, None)

# Example usage:
if __name__ == "__main__":
    # Example calls to the function demonstrating the return of a tuple with validity and number
    print(is_valid_number("123"))  # Should return (True, 123)
    print(is_valid_number("-123.45"))  # Should return (True, -123.45)
    print(is_valid_number("abc"))  # Should return (False, None)
    print(is_valid_number("123" * 50))  # Should return (False, None) due to length
    print(is_valid_number(123))  # Should return (True, 123)
    print(is_valid_number(123.45))  # Should return (True, 123.45)

