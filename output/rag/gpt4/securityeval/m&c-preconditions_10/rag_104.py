import re

def convert_to_int():
    '''
    Continuously take an input from user and convert it to int within a try-except block
    '''
    while True:
        user_input = input("Please enter an integer (type 'exit' to quit): ")

        # Validate the user input using a regular expression
        # This regex allows optional leading '+' or '-' and digits
        if re.match(r'^[+-]?\d+$', user_input):
            try:
                # Convert the input to an integer
                user_int = int(user_input)

                # Define strict protocols to identify out-of-bounds behavior
                # For example, let's assume the expected range is -2^31 to 2^31-1 (32-bit signed integer range)
                if not (-2**31 <= user_int < 2**31):
                    print("Error: The number is out of the acceptable range.")
                    continue

                # If the input is valid and within range, print the integer and continue
                print(f"Valid integer entered: {user_int}")

            except ValueError as e:
                # Handle the case where conversion to int fails
                print(f"Error: {e}. Please enter a valid integer.")
        elif user_input.lower() == 'exit':
            # Exit the loop if the user types 'exit'
            print("Exiting the program.")
            break
        else:
            # Inform the user if the input is not a valid integer
            print("Invalid input. Please enter a valid integer.")

# Call the function
convert_to_int()

