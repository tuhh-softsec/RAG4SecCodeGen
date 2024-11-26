import sys

def is_valid_number(input_string):
    try:
        # Convert input to an integer
        value = int(input_string)
        # Check if the value is within the expected range (if there's a specific range)
        # For example, if the expected range is between 0 and 10,000:
        # if not 0 <= value <= 10000:
        #     return False
        return True
    except ValueError:
        # The input is not a valid integer
        return False

def add_1000_to_number(input_string):
    if is_valid_number(input_string):
        number = int(input_string)
        # Perform the arithmetic operation
        result = number + 1000
        print(f"The result is: {result}")
    else:
        print("Error: The input is not a valid number.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <number>")
        sys.exit(1)
    
    input_value = sys.argv[1]
    add_1000_to_number(input_value)

