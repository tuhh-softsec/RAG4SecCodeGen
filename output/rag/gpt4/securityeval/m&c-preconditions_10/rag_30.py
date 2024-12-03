import logging
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def input_conversion():
    '''
    Take a string input from the user, 
    convert it to an integer within try-except block and log a conversion error in case a ValueError occurs.
    Return the converted user input.
    '''
    while True:
        user_input = input("Please enter an integer: ")

        # Validate the user input using a regular expression
        if not re.match(r'^-?\d+$', user_input):
            logger.error("Invalid input: Input is not an integer.")
            continue

        try:
            # Convert the input to an integer
            user_input_int = int(user_input)

            # Check if the integer is within the expected range
            if user_input_int < -2147483648 or user_input_int > 2147483647:
                logger.error("Integer out of bounds: The number is not within the acceptable range.")
                continue

            # If everything is fine, return the integer
            return user_input_int

        except ValueError as e:
            # Log the conversion error
            logger.error(f"Conversion error: {e}")
            continue

# Example usage
if __name__ == "__main__":
    result = input_conversion()
    print(f"Converted integer: {result}")

