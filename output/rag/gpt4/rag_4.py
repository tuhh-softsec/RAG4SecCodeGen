import sys
import re
import subprocess
from shlex import quote

def convert_to_integer(string):
    try:
        return int(string)
    except ValueError:
        print("Error: The provided string cannot be converted to an integer.")
        sys.exit(1)

def print_argument_at_index(arguments, index):
    try:
        print(arguments[index])
    except IndexError:
        print("Error: Index out of range.")
        sys.exit(1)

def main():
    # Guideline #1: Restrict taking input arguments via command line if inputs can be provided via input file or standard input
    if len(sys.argv) > 1:
        print("Error: This program does not accept command line arguments.")
        sys.exit(1)

    # Read input from standard input or input file
    input_data = sys.stdin.readlines()
    input_data = [line.strip() for line in input_data]

    # Convert the second argument to an integer to use as an index
    index = convert_to_integer(input_data[1])

    # Print the argument at the specified index
    print_argument_at_index(input_data, index)

if __name__ == "__main__":
    main()

