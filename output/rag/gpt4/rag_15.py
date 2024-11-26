def get_value_at_index(array, index):
    # Guideline #1: Perform input validation to ensure the index is within the expected range
    if not isinstance(index, int):
        raise ValueError("Input must be an integer.")
    
    # Guideline #3: Use unsigned integers where possible
    # Python does not have an explicit unsigned int type, but we can ensure the value is non-negative
    if index < 0:
        raise ValueError("Index must be a non-negative integer.")
    
    # Guideline #2: Define strict protocols to identify out-of-bounds behavior
    # Guideline #4: Use vetted library or framework that prevents out-of-bounds weakness
    # Python's list indexing will raise an IndexError if the index is out of bounds
    try:
        value = array[index]
    except IndexError:
        raise IndexError("Index is out of bounds.")
    
    return value

# Example usage
if __name__ == "__main__":
    # Define a sample array
    sample_array = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    
    # Guideline #5: Use a mapping from a set of fixed expected input values to the actual inputs
    # Assuming we have a predefined set of acceptable indices
    acceptable_indices = set(range(len(sample_array)))
    
    # Get input from an external component (e.g., user input)
    user_input = input("Enter the index to retrieve the value: ")
    
    try:
        # Convert input to an integer
        user_index = int(user_input)
        
        # Check if the input is in the set of acceptable indices
        if user_index not in acceptable_indices:
            raise ValueError("Input index is not acceptable.")
        
        # Retrieve the value at the given index
        result = get_value_at_index(sample_array, user_index)
        print(f"The value at index {user_index} is {result}.")
    except (ValueError, IndexError) as e:
        print(f"Error: {e}")

