import re

def convert_to_int():
    '''
    Take an input from the user (console) and convert it to int within a try-except block.
    Validate the user input using regular expressions and ensure that the input is within an expected range.
    '''

    # Define the expected range for the integer input
    MIN_INT_VALUE = -2147483648  # Minimum value for a 32-bit signed integer
    MAX_INT_VALUE = 2147483647   # Maximum value for a 32-bit signed integer

    # Regular expression to match a valid signed integer input
    valid_integer_regex = r'^[-+]?\d+$'

    while True:
        user_input = input("Please enter an integer: ")

        # Validate the input using the regular expression
        if not re.match(valid_integer_regex, user_input):
            print("Invalid input. Please enter a valid integer.")
            continue

        try:
            # Convert the input to an integer
            user_int = int(user_input)

            # Check if the integer is within the expected range
            if user_int < MIN_INT_VALUE or user_int > MAX_INT_VALUE:
                print(f"Input is out of bounds. Please enter a value between {MIN_INT_VALUE} and {MAX_INT_VALUE}.")
                continue

            # If input is valid and within range, return the integer
            return user_int

        except ValueError:
            # Handle the case where conversion to integer fails
            print("Conversion to integer failed. Please enter a valid integer.")
            continue

# Example usage
if __name__ == "__main__":
    result = convert_to_int()
    print(f"The converted integer is: {result}")

