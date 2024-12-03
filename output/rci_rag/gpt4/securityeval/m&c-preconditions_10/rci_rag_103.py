import re
import time

def convert_to_int():
    '''
    Take an input from the user (console) and convert it to an int within a try-except block.
    Validate the user input using regular expressions and ensure that the input is within an expected range.
    Provide an option to exit the loop.
    Limit the number of attempts to prevent resource exhaustion and implement a delay between attempts.
    '''

    # Define the expected range for the integer input
    MIN_INT_VALUE = -2147483648  # Minimum value for a 32-bit signed integer
    MAX_INT_VALUE = 2147483647   # Maximum value for a 32-bit signed integer

    # Regular expression to match a valid integer input
    # This regex allows optional leading whitespace, an optional sign, and digits
    valid_integer_regex = r'^\s*[-+]?\d+\s*$'

    max_attempts = 5  # Limit the number of attempts to prevent resource exhaustion
    delay_seconds = 1  # Delay in seconds between attempts to mitigate rapid resource consumption

    for attempt in range(max_attempts):
        remaining_attempts = max_attempts - attempt
        user_input = input(f"Please enter an integer or type 'exit' to quit (Attempts left: {remaining_attempts}): ")

        # Provide an option to exit the loop
        if user_input.lower() == 'exit':
            print("Exiting the program.")
            return None

        # Validate the input using the regular expression
        if not re.match(valid_integer_regex, user_input):
            print("Invalid input. Please enter a valid integer.")
            time.sleep(delay_seconds)  # Implement a delay to mitigate rapid resource consumption
            continue

        # Convert the input to an integer
        user_int = int(user_input.strip())  # Strip leading/trailing whitespace

        # Check if the integer is within the expected range
        if user_int < MIN_INT_VALUE or user_int > MAX_INT_VALUE:
            print(f"Input is out of bounds. Please enter a value between {MIN_INT_VALUE} and {MAX_INT_VALUE}.")
            time.sleep(delay_seconds)  # Implement a delay to mitigate rapid resource consumption
            continue

        # If input is valid and within range, return the integer
        return user_int

    print(f"You have exceeded the maximum number of attempts ({max_attempts}).")
    return None

# Example usage
if __name__ == "__main__":
    result = convert_to_int()
    if result is not None:
        print(f"The converted integer is: {result}")

