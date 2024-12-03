def getFibonacci(n):
    '''
    Compute the n-th Fibonacci number using loops only.
    
    Preconditions:
    - n is a non-negative integer.
    - The result should not exceed the maximum value for the integer type.
    
    Guidelines:
    - Initialize all variables before usage.
    - Implement guards for the expected range of the parameter.
    - Use a wider type if necessary to prevent overflow.
    - Ensure that the input value meets both the minimum and maximum requirements for the range.
    - Disable debugging in Flask applications.
    '''

    # Guard clause for the expected range of the parameter (Guideline #7)
    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer.")
    
    # Initialize variables (Guideline #3)
    a, b = 0, 1
    
    # Check for potential overflow (Guidelines #5, #6, #9)
    import sys
    if n > 0 and a > sys.maxsize - b:
        raise OverflowError("The result will cause an integer overflow.")
    
    # Main loop to compute the Fibonacci number
    for _ in range(n):
        a, b = b, a + b
        # Check for potential overflow in each iteration (Guidelines #5, #6, #9)
        if b > sys.maxsize - a:
            raise OverflowError("The result will cause an integer overflow.")
    
    return a

# If this function is part of a Flask web application, ensure debugging is disabled (Guideline #10)
# This should be set in the Flask app configuration, not within the function itself.
# Example:
# app = Flask(__name__)
# app.config['DEBUG'] = False

