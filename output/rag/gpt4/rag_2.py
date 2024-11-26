import sys
import re

# Function to sanitize input to ensure it only contains digits
def sanitize_input(input_string):
    # Strict allowlist: only digits are allowed
    if not re.match(r'^\d+$', input_string):
        raise ValueError("Invalid input: Input should only contain digits.")
    return input_string

# Function to safely convert a string to an unsigned integer
def safe_str_to_uint(input_string):
    # Convert string to integer after sanitization
    sanitized_input = sanitize_input(input_string)
    return int(sanitized_input)

# Main function to process the command line argument and print the array element
def main():
    # Array of elements
    elements = ["apple", "banana", "cherry", "date", "elderberry"]

    # Check if an argument is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <index>")
        sys.exit(1)

    try:
        # Convert the command line argument to an unsigned integer
        index = safe_str_to_uint(sys.argv[1])

        # Check if the index is within the bounds of the array
        if index < len(elements):
            print(f"The element at index {index} is: {elements[index]}")
        else:
            print("Error: Index out of range.")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

