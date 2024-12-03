import logging
import logging.config
import os
import time

# Define a centralized logging configuration
def setup_logging():
    logging_config = {
        'version': 1,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'fileHandler': {
                'class': 'logging.FileHandler',
                'formatter': 'standard',
                'filename': os.environ.get('LOG_FILE_PATH', 'app.log'),
                'mode': 'a',
                'encoding': 'utf-8',
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['fileHandler'],
                'level': os.environ.get('LOG_LEVEL', 'INFO'),
                'propagate': False
            }
        }
    }
    logging.config.dictConfig(logging_config)

setup_logging()

def convert_to_int(max_attempts=3, timeout=10):
    '''
    Take an input from the user (console) and convert it to an integer within a try-except block.
    Includes input validation, limits the number of attempts, and implements a timeout.
    '''
    attempts = 0
    start_time = time.time()
    while attempts < max_attempts:
        if time.time() - start_time > timeout:
            logging.error("Function call timed out.")
            print("Operation timed out. Please try again later.")
            return None  # or raise an appropriate exception

        user_input = input("Please enter a number: ")
        try:
            user_int = int(user_input)
            # Add any additional input validation here (e.g., range checks)
            print(f"The integer value is {user_int}")
            return user_int
        except ValueError:
            attempts += 1
            print(f"The input is not a valid integer. Please try again. ({attempts}/{max_attempts} attempts)")
            logging.warning(f"Invalid input: {user_input}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            print("An unexpected error occurred. Please contact support.")
            return None  # or handle the exception accordingly
    else:
        print("Maximum attempts reached. Please ensure the input is a valid integer.")
        logging.error("Maximum attempts reached without a valid input.")
        return None

# Call the function
convert_to_int()

