import re
import logging
from time import sleep

# Constants for integer range
MIN_INT = -2147483648
MAX_INT = 2147483647
EXIT_COMMAND = 'exit'
ATTEMPT_LIMIT = 5
RATE_LIMIT_SEC = 1

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')
logger = logging.getLogger()

def input_with_rate_limit(prompt, rate_limit_sec):
    """
    Enforces a rate limit between inputs.
    """
    sleep(rate_limit_sec)
    return input(prompt)

def convert_to_int():
    '''
    Continuously take an input from user and convert it to int within a try-except block
    with input validation to ensure security.
    '''

    # Regular expression to match a valid integer input
    # This regex will match optional sign followed by digits without leading zeros
    valid_integer_regex = re.compile(r'^[+-]?(0|[1-9]\d*)$')

    attempts = 0

    while attempts < ATTEMPT_LIMIT:
        user_input = input_with_rate_limit(f"Enter an integer within the range {MIN_INT} to {MAX_INT} (or '{EXIT_COMMAND}' to quit): ", RATE_LIMIT_SEC)

        # Check if the user wants to exit the loop
        if user_input.lower() == EXIT_COMMAND:
            logger.info("User exited the program.")
            print("Exiting the program.")
            break

        # Validate the user input using the regular expression
        if not valid_integer_regex.match(user_input):
            logger.warning("Invalid input detected.")
            print("Invalid input. Please enter a valid integer without leading zeros.")
            attempts += 1
            continue

        try:
            # Convert the input to an integer
            user_input_int = int(user_input)

            # Check for out-of-bounds behavior
            if user_input_int < MIN_INT or user_input_int > MAX_INT:
                logger.warning("Number out of bounds detected.")
                print(f"The number is out of bounds. Please enter a number within the range {MIN_INT} to {MAX_INT}.")
                attempts += 1
                continue

            # If the input is valid and within bounds, print the converted integer
            logger.info("Converted integer successfully.")
            print(f"Converted integer: {user_input_int}")
            attempts = 0  # Reset attempts after a successful conversion

        except ValueError as e:
            # Handle the exception if conversion to integer fails
            logger.error("An error occurred during conversion.")
            print("An error occurred. Please enter a valid integer.")
            attempts += 1

    if attempts >= ATTEMPT_LIMIT:
        logger.error("User reached maximum attempt limit.")
        print("You have reached the maximum number of invalid attempts. Exiting the program.")

# Call the function
convert_to_int()

