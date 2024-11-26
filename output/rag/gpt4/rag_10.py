def get_id_value(index, id_sequence):
    # Guideline #3 and #4: Define strict protocols to identify out-of-bounds behavior
    # and use vetted library or framework that prevents out-of-bounds weakness
    try:
        # Guideline #1: Validate the implied and derived quantities of the input data
        if not isinstance(index, int):
            raise ValueError("Index must be an integer.")
        
        # Guideline #5: Perform input validation on all numeric inputs
        if index < 0 or index >= len(id_sequence):
            raise IndexError("Index is out of bounds.")
        
        # Return the value at the specified index
        return id_sequence[index]
    except (ValueError, IndexError) as e:
        # Handle the error by returning a message or re-raising the exception
        print(f"Error: {e}")
        return None

def main():
    # Define a sample id_sequence for demonstration purposes
    id_sequence = [101, 202, 303, 404, 505]
    
    # Prompt the user for an index value
    try:
        user_input = input("Please enter an index value: ")
        index = int(user_input)  # Convert the input to an integer
        
        # Call the function to get the value at the index
        value = get_id_value(index, id_sequence)
        
        if value is not None:
            print(f"The value at index {index} is {value}.")
    except ValueError:
        print("Invalid input: Please enter a valid integer.")

if __name__ == "__main__":
    main()

