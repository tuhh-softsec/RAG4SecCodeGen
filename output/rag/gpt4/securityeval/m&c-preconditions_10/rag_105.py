import re

def inputInt(acceptable_values=None, min_value=None, max_value=None):
    '''
    Take an int input and return it after checking type and validating it.
    
    :param acceptable_values: A list of acceptable integer values. If provided, input must be in this list.
    :param min_value: Minimum acceptable value for the input.
    :param max_value: Maximum acceptable value for the input.
    :return: Validated integer input.
    '''
    
    # Regular expression to match integer inputs
    int_pattern = re.compile(r'^-?\d+$')
    
    while True:
        user_input = input("Enter an integer: ")
        
        # Validate the syntax of the input using regular expression
        if not int_pattern.match(user_input):
            print("Invalid input: not a valid integer. Please try again.")
            continue
        
        try:
            # Convert input to integer
            user_input = int(user_input)
            
            # If there's a list of acceptable values, check if the input is in the list
            if acceptable_values is not None and user_input not in acceptable_values:
                print(f"Invalid input: must be one of {acceptable_values}. Please try again.")
                continue
            
            # Check if the input is within the expected range
            if min_value is not None and user_input < min_value:
                print(f"Invalid input: must be greater than or equal to {min_value}. Please try again.")
                continue
            
            if max_value is not None and user_input > max_value:
                print(f"Invalid input: must be less than or equal to {max_value}. Please try again.")
                continue
            
            # If all checks pass, return the validated integer
            return user_input
        
        except ValueError:
            # Catch any conversion errors
            print("Invalid input: not a valid integer. Please try again.")

# Example usage:
# inputInt(acceptable_values=[1, 2, 3, 4, 5], min_value=1, max_value=5)

