import logging
import os

# Define a function to configure logging
def configure_logging(log_directory="/var/log/my_application"):
    log_filename = "conversion.log"
    log_filepath = os.path.join(log_directory, log_filename)
    
    # Set restrictive permissions on new directories and reset umask after creation
    old_umask = os.umask(0o077)
    try:
        # Use exist_ok to mitigate race conditions
        os.makedirs(log_directory, exist_ok=True)
    except OSError as e:
        logging.error(f"Failed to create log directory: {e}")
        raise
    finally:
        os.umask(old_umask)  # Reset umask to its original value
    
    # Configure logging with a more flexible approach
    logging.basicConfig(
        filename=log_filepath,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Call the function to configure logging at the start of the application
try:
    configure_logging()
except Exception as e:
    print(f"Failed to configure logging: {e}")
    exit(1)

def inputConversion():
    '''
    Take a string input from the user, 
    convert it to an integer within try-except block and log a conversion error in case a ValueError occurs.
    Return the converted user input or None if conversion fails.
    '''
    try:
        # Prompt the user for input
        user_input = input("Please enter a number: ")
        # Perform robust input validation
        if not user_input.isdigit() or int(user_input) <= 0:
            raise ValueError("Input is not a valid positive integer.")
        # Attempt to convert the input to an integer
        converted_input = int(user_input)
        return converted_input
    except ValueError as e:
        # Log the error without including the user input
        logging.error(f"Error converting user input to an integer: {str(e)}")
        return None
    except Exception as e:
        # Log unexpected errors
        logging.error(f"Unexpected error: {str(e)}")
        return None

# Example usage:
if __name__ == "__main__":
    result = inputConversion()
    if result is not None:
        print(f"The converted number is {result}.")
    else:
        print("Conversion failed. Please enter a valid number.")

