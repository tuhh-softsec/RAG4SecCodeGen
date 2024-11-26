import sys
import re

def read_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def sanitize_input(input_string):
    # Allowlist: alphanumeric characters, spaces, and underscores
    pattern = re.compile(r'^[\w\s]+$')
    if not pattern.match(input_string):
        raise ValueError("Invalid input detected!")
    return input_string

def get_value_at_index(input_source, index):
    try:
        # Read input from file or standard input
        if input_source == 'file':
            file_path = input("Enter the file path: ")
            input_list = read_input_from_file(file_path)
        else:
            input_list = sys.stdin.readlines()

        # Sanitize and convert index to integer
        sanitized_index = int(sanitize_input(index.strip()))

        # Access the value at the sanitized index
        value = sanitize_input(input_list[sanitized_index].strip())
        return value
    except (ValueError, IndexError) as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Check if the input should come from a file or standard input
    input_source = input("Enter 'file' to read from a file, or 'stdin' to read from standard input: ").strip().lower()
    if input_source not in ['file', 'stdin']:
        print("Invalid input source. Please enter 'file' or 'stdin'.")
        sys.exit(1)

    # Prompt for the index
    index = input("Enter the index of the value you want to retrieve: ")

    # Retrieve and print the value at the given index
    value = get_value_at_index(input_source, index)
    if value is not None:
        print(f"The value at index {index} is: {value}")

