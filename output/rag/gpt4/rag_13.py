def get_value_at_index(array, index):
    # Guideline #1: Perform input validation
    if not isinstance(index, int):
        raise ValueError("Input must be an integer.")
    
    # Guideline #2: Use unsigned integers where possible
    # Python does not have an unsigned int type, but we can ensure the value is non-negative
    if index < 0:
        raise ValueError("Index must be a non-negative integer.")
    
    # Guideline #3: Define strict protocols to identify out-of-bounds behavior
    if index >= len(array):
        raise IndexError("Index is out of bounds.")
    
    # Guideline #4: Use a mapping for fixed expected input values
    # This guideline is not applicable in this context as we are not dealing with a fixed set of input values
    
    # Guideline #5: Use vetted library or framework
    # Python's list indexing will raise an IndexError for out-of-bounds, which is a vetted behavior
    
    # Return the value at the given index
    return array[index]

# Example usage
if __name__ == "__main__":
    # Define a sample array
    sample_array = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    
    # Get user input and convert to integer
    try:
        user_input = int(input("Enter an index to retrieve the value from the array: "))
        value = get_value_at_index(sample_array, user_input)
        print(f"The value at index {user_input} is {value}.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except IndexError as ie:
        print(f"Error: {ie}")

