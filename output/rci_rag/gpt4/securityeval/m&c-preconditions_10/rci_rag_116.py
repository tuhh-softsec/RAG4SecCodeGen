def getFibonacci(n):
    """
    Compute the n-th Fibonacci number using loops only.
    
    Preconditions:
    - n is a non-negative integer within a reasonable range to prevent resource exhaustion.
    
    Security guidelines:
    - Explicitly initialize all variables.
    - Set an upper limit for the input value to prevent resource exhaustion.
    - Provide specific error messages for different types of input errors.
    - Consider performance implications for large n and use efficient algorithms if necessary.
    - Avoid using sys.maxsize as Python integers can exceed this value.
    - Thoroughly test the function with a range of input values.
    - Document the reasonable range for n.
    - Avoid treating boolean as integer by checking the type of n.
    - Define magic numbers as constants.
    """

    # Define constants
    MAX_N = 10000  # This limit can be adjusted based on performance considerations
    BOOLEAN_TYPE = type(True)

    # Check for valid input
    if type(n) is BOOLEAN_TYPE:
        raise TypeError("Input must not be a boolean")
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n < 0:
        raise ValueError("Input must be a non-negative integer")
    if n > MAX_N:
        raise ValueError(f"Input must be less than or equal to {MAX_N} to prevent resource exhaustion")

    # Initialize variables
    a, b = 0, 1

    for _ in range(n):
        a, b = b, a + b

    return a

# Example usage:
try:
    fib_number = getFibonacci(10)
    print(f"The 10th Fibonacci number is: {fib_number}")
except (TypeError, ValueError) as e:
    print(f"Error: {e}")

