import sys
import time
import logging

# Configure logging
logging.basicConfig(filename='inputInt.log', level=logging.INFO, format='%(asctime)s %(message)s')

def inputInt(acceptable_values=None, min_value=None, max_value=None, max_attempts=3):
    '''
    Take an int input and return it after checking type and validating against
    provided constraints. Allows the user to exit after a certain number of failed attempts.

    :param acceptable_values: A list of acceptable integer values. If provided, the input must be in this list.
    :param min_value: The minimum acceptable value for the input. If provided, the input must be greater than or equal to this value.
    :param max_value: The maximum acceptable value for the input. If provided, the input must be less than or equal to this value.
    :param max_attempts: The maximum number of input attempts before exiting. Default is 3.
    :return: The validated integer input from the user or a unique sentinel value if the maximum number of attempts is reached.
    '''
    attempts = 0
    while attempts < max_attempts:
        try:
            user_input = input(f"Please enter an integer (or 'quit' to exit). Attempts remaining: {max_attempts - attempts}: ")
            if user_input.lower() == 'quit':
                print("User requested to exit.")
                return None

            # Sanitize input to prevent command injection or other exploits
            sanitized_input = user_input.strip()

            user_int = int(sanitized_input)

            if acceptable_values is not None and user_int not in acceptable_values:
                raise ValueError("Input is not in the list of acceptable values.")

            if min_value is not None and user_int < min_value:
                raise ValueError(f"Input is less than the minimum value of {min_value}.")

            if max_value is not None and user_int > max_value:
                raise ValueError(f"Input is greater than the maximum value of {max_value}.")

            return user_int

        except ValueError as e:
            print("Invalid input. Please try again.")
            logging.warning(f"Invalid input: {e}")
            attempts += 1
            time.sleep(1)  # Implement a delay to mitigate rapid repeated attempts
        except OverflowError:
            print("The number entered is too large.")
            logging.error("OverflowError: The number entered is too large.")
            attempts += 1
            time.sleep(1)  # Implement a delay to mitigate rapid repeated attempts

    logging.error(f"Maximum number of attempts ({max_attempts}) reached. Exiting.")
    print(f"Maximum number of attempts ({max_attempts}) reached. Exiting.")
    return 'MAX_ATTEMPTS_REACHED'  # Use a unique sentinel value to indicate this condition

# Example usage:
# result = inputInt(min_value=1, max_value=100)
# if result != 'MAX_ATTEMPTS_REACHED':
#     print(f"Validated integer: {result}")
# else:
#     print("No valid input received after maximum attempts.")

