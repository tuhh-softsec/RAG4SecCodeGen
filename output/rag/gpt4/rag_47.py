import sys
import re

def sanitize_input(input_string):
    # Define an allowlist of characters (alphanumeric and some punctuation)
    allowlist = re.compile(r'[a-zA-Z0-9\s\.\,\-\_]+')
    
    # Match the input string against the allowlist
    sanitized = allowlist.match(input_string)
    
    # If the input string contains only allowlisted characters, return it
    if sanitized:
        return sanitized.group()
    else:
        raise ValueError("Invalid characters in input")

def main():
    # Check if an argument is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <argument>")
        sys.exit(1)
    
    # Get the command line argument
    input_arg = sys.argv[1]
    
    # Sanitize the input to ensure it only contains allowlisted characters
    try:
        safe_input = sanitize_input(input_arg)
    except ValueError as e:
        print(str(e))
        sys.exit(1)
    
    # Trim trailing whitespace characters
    trimmed_input = safe_input.rstrip()
    
    # Print the sanitized and trimmed input to the console
    # Using repr() to ensure proper output encoding and escaping
    print(repr(trimmed_input))

if __name__ == "__main__":
    main()

