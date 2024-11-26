import random
import sys

# Function to generate a random unsigned integer between min_val and max_val
def generate_random_unsigned_integer(min_val, max_val):
    if min_val < 0 or max_val < 0:
        raise ValueError("Only unsigned integers are allowed")
    if min_val >= max_val:
        raise ValueError("Minimum value must be less than maximum value")
    return random.randint(min_val, max_val)

# Function to calculate the difference between two unsigned integers
def calculate_difference_unsigned(a, b):
    if a < b:
        raise ValueError("First number must be greater than or equal to the second number to avoid negative results")
    return a - b

# Function to validate that the input is an unsigned integer within the expected range
def validate_unsigned_integer_input(value, min_val, max_val):
    if not isinstance(value, int):
        raise TypeError("Input must be an integer")
    if value < min_val or value > max_val:
        raise ValueError("Input is out of bounds")
    return value

# Main code
try:
    # Generate two random unsigned integers between 10 and 1000
    num1 = generate_random_unsigned_integer(10, 1000)
    num2 = generate_random_unsigned_integer(10, 1000)

    # Validate the generated numbers
    num1 = validate_unsigned_integer_input(num1, 10, 1000)
    num2 = validate_unsigned_integer_input(num2, 10, 1000)

    # Calculate the difference between the two numbers
    difference = calculate_difference_unsigned(max(num1, num2), min(num1, num2))

    # Print the results
    print(f"The first random number is: {num1}")
    print(f"The second random number is: {num2}")
    print(f"The difference between the two numbers is: {difference}")

except ValueError as ve:
    print(f"ValueError: {ve}", file=sys.stderr)
except TypeError as te:
    print(f"TypeError: {te}", file=sys.stderr)

