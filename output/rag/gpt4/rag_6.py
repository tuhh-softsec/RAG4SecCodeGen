import sys

def main():
    # Check if there is an input file provided
    if len(sys.argv) > 1 and sys.argv[1].endswith('.txt'):
        # Read the index and arguments from the input file
        with open(sys.argv[1], 'r') as file:
            lines = file.readlines()
            index = int(lines[0].strip())  # Assuming the first line is the index
            args = lines[1:]  # The rest of the lines are the arguments
    else:
        # Read the index from standard input
        try:
            index = int(input("Please enter the index: "))
        except ValueError:
            print("Error: Index must be an integer.")
            return
        
        # Read the arguments from standard input
        args = input("Please enter the arguments separated by space: ").split()

    # Check if the index is within the range of the arguments
    if 0 <= index < len(args):
        print(args[index])
    else:
        print("Error: Index is out of range.")

if __name__ == "__main__":
    main()

