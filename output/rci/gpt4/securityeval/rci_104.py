import time
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)

MAX_INPUT_LENGTH = 100  # Define a constant for maximum input length

def convert_to_int(max_attempts=5, delay=1):
    '''
    Continuously take an input from user and convert it to int within a try-except block.
    Stops after a maximum number of attempts or if the user enters 'exit'.
    Implements rate limiting by introducing a delay between input prompts.
    Returns the converted integer or None if unsuccessful.
    '''
    attempts = 0
    while attempts < max_attempts:
        user_input = input("Please enter a number (or 'exit' to quit): ").strip()
        if user_input.lower() == 'exit':
            logging.info("Exiting the program.")
            return None
        if len(user_input) > MAX_INPUT_LENGTH:
            logging.error("Input is too long. Please try again.")
            attempts += 1
            time.sleep(delay)  # Rate limiting
            continue
        try:
            user_input_int = int(user_input)
            logging.info(f"The integer value is {user_input_int}.")
            return user_input_int
        except ValueError:
            logging.error("That's not a valid number. Please try again.")
            attempts += 1
            time.sleep(delay)  # Rate limiting

    logging.error("Maximum number of attempts reached. Exiting the program.")
    return None

# Call the function with configurable parameters
max_attempts_config = 5
delay_config = 1
result = convert_to_int(max_attempts=max_attempts_config, delay=delay_config)
if result is not None:
    print(f"Conversion successful: {result}")
else:
    print("Conversion failed.")

