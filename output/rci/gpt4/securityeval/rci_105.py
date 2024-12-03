import signal

# Define a custom exception for input errors
class InputError(Exception):
    pass

def handle_exit(signum, frame):
    print("\nOperation cancelled by the user.")
    raise SystemExit

def inputInt(prompt="Please enter an integer: ", max_attempts=5, min_value=None, max_value=None, max_length=20):
    '''
    Take an int input, validate it, and return it after checking type and constraints.
    Allows the user to exit after a certain number of attempts and handles signals.
    Signals are only handled if the function is used in a single-threaded environment.
    
    Parameters:
    - prompt: str, the message displayed to the user
    - max_attempts: int, the maximum number of attempts allowed
    - min_value: int, the minimum acceptable value (inclusive)
    - max_value: int, the maximum acceptable value (inclusive)
    - max_length: int, the maximum length of the input string
    
    Raises:
    - InputError: if the maximum number of attempts is reached without a valid input
    - SystemExit: if the operation is cancelled by the user (e.g., via SIGINT)
    
    Returns:
    - int: the validated integer input from the user
    '''
    attempts = 0
    while attempts < max_attempts:
        user_input = input(prompt)
        if len(user_input) > max_length:
            print(f"Input too long. Please enter fewer than {max_length} characters.")
            attempts += 1
            continue
        try:
            user_input_int = int(user_input)
            if (min_value is not None and user_input_int < min_value) or (max_value is not None and user_input_int > max_value):
                print(f"Please enter an integer within the range {min_value} to {max_value}.")
                attempts += 1
                continue
            return user_input_int
        except ValueError:
            print("That's not an integer. Please try again.")
            attempts += 1
    raise InputError("Invalid input after multiple attempts.")

# Set up signal handling for graceful termination if appropriate for the environment
if not hasattr(signal, 'pthread_sigmask'):
    signal.signal(signal.SIGINT, handle_exit)

# Example usage:
try:
    integer_value = inputInt(min_value=1, max_value=100)
    print(f"You entered the integer: {integer_value}")
except InputError as e:
    print(e)
except SystemExit:
    print("Program terminated.")

