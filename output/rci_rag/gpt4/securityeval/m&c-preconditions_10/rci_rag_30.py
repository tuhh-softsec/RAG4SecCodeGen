import logging
import re
import sys
import signal

# Configure logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def input_conversion(min_value=-2**31, max_value=2**31-1, max_attempts=5):
    '''
    Take a string input from the user, 
    convert it to an integer within a specific range, and handle conversion errors.
    Return the converted user input or None if the user chooses to exit or max attempts are reached.
    '''
    attempts = 0
    prompt = f"Please enter an integer ({min_value} to {max_value}), or type 'exit' to quit: "
    
    def signal_handler(signum, frame):
        print("\nSignal received, exiting the program.")
        sys.exit(0)

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while attempts < max_attempts:
        try:
            user_input = input(prompt)

            # Allow the user to exit the loop
            if user_input.lower() in ['exit', 'quit']:
                print("Exiting the program.")
                return None

            # Validate the user input using regular expressions
            if not re.match(r'^-?\d+$', user_input):
                logger.error("Invalid input: Input is not a valid integer.")
                attempts += 1
                continue

            # Convert the input to an integer
            user_input_int = int(user_input)

            # Check if the integer is within the expected range
            if not min_value <= user_input_int <= max_value:
                logger.error(f"Conversion error: Integer out of bounds ({min_value} to {max_value}).")
                attempts += 1
                continue

            # If conversion is successful and within bounds, return the integer
            return user_input_int

        except ValueError:
            # Log the error without sensitive information
            logger.error("Conversion error: Invalid input format.")
            attempts += 1
        except KeyboardInterrupt:
            # Handle KeyboardInterrupt (Ctrl+C) and exit gracefully
            print("\nInterrupt received, exiting the program.")
            sys.exit(0)

    print(f"Maximum attempts ({max_attempts}) reached. Exiting the program.")
    return None

# Example usage
if __name__ == "__main__":
    result = input_conversion()
    if result is not None:
        print(f"Converted integer: {result}")

