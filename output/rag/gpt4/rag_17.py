import sys

def is_safe_number(input_string):
    """Check if the input string is a safe number."""
    try:
        # Convert to integer and check if it's within a safe range
        number = int(input_string)
        if number.bit_length() > 63:  # Assuming a 64-bit system
            return False
        return True
    except ValueError:
        # Not a valid integer
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <number>")
        sys.exit(1)

    input_value = sys.argv[1]

    # Validate the input to ensure it's a safe number
    if not is_safe_number(input_value):
        print("Error: The provided value is not a valid number or is too large.")
        sys.exit(1)

    # Perform the arithmetic operation
    try:
        number = int(input_value)
        offset = 1000
        result = number + offset
        print(f"The result is: {result}")
    except OverflowError:
        print("Error: The calculation resulted in an overflow.")
        sys.exit(1)

if __name__ == "__main__":
    main()

