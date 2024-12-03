import sys
import logging

# Configure logging
logging.basicConfig(filename='fibonacci.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Define a maximum allowed value for n to prevent resource exhaustion
MAX_ALLOWED_VALUE = 10000

def getFibonacci(n):
    '''
    Compute the n-th Fibonacci number using loops only.

    Parameters:
    n (int): The position in the Fibonacci sequence to compute.

    Returns:
    int: The n-th Fibonacci number.

    Raises:
    ValueError: If the input is not a non-negative integer or exceeds the maximum allowed value.
    '''

    # Check if the input is an integer and within the allowed range
    if not isinstance(n, int) or n < 0 or n > MAX_ALLOWED_VALUE:
        raise ValueError(f"Input must be a non-negative integer less than or equal to {MAX_ALLOWED_VALUE}")

    # Handle the base cases
    if n == 0:
        return 0
    elif n == 1:
        return 1

    # Initialize the first two Fibonacci numbers
    a, b = 0, 1

    # Compute the Fibonacci numbers iteratively
    for _ in range(2, n + 1):
        a, b = b, a + b

    return b

# Example usage:
if __name__ == "__main__":
    try:
        # Accept dynamic input, with appropriate validation and error handling
        if len(sys.argv) != 2:
            logging.error("Incorrect number of arguments")
            print(f"Usage: python {sys.argv[0]} <non-negative integer>")
            sys.exit(1)

        # Input sanitization and validation
        input_value = sys.argv[1]
        if not input_value.isdigit():
            logging.error("Input is not a digit")
            raise ValueError("Input must be a digit")

        n = int(input_value)
        if n < 0 or n > MAX_ALLOWED_VALUE:
            logging.error("Input is out of the allowed range")
            raise ValueError(f"Input must be a non-negative integer less than or equal to {MAX_ALLOWED_VALUE}")

        result = getFibonacci(n)
        print(f"The {n}-th Fibonacci number is: {result}")
        logging.info(f"Computed the {n}-th Fibonacci number: {result}")
    except ValueError as e:
        logging.exception("ValueError encountered")
        print(f"Error: {e}")
        sys.exit(2)
    except Exception as e:
        logging.exception("An unexpected error occurred")
        print(f"An unexpected error occurred: {e}")
        sys.exit(3)

