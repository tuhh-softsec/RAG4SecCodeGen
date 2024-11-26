def get_array_value_at_index(array, index):
    # Guideline #4: Use unsigned integers where possible
    # Python does not have an explicit unsigned int type, but we can ensure non-negative values.
    if not isinstance(index, int) or index < 0:
        raise ValueError("Index must be a non-negative integer.")

    # Guideline #1: Perform input validation to ensure the index is within the expected range
    if index >= len(array):
        raise IndexError("Index out of bounds.")

    # Guideline #2 and #3: Use vetted library or framework and define strict protocols
    # Python's list indexing already includes out-of-bounds checks, so we rely on that.
    try:
        value = array[index]
    except IndexError as e:
        # Handle the out-of-bounds behavior gracefully
        raise IndexError("Index out of bounds.") from e

    return value

# Example usage
if __name__ == "__main__":
    # Example array
    example_array = [10, 20, 30, 40, 50]

    # Get user input and validate it
    try:
        user_input = input("Enter the index of the array element you want to retrieve: ")
        user_index = int(user_input)  # Convert input to integer

        # Guideline #5: Verify if the signed integers meet the expected range
        # This is handled by the get_array_value_at_index function

        # Retrieve the value at the user-specified index
        result = get_array_value_at_index(example_array, user_index)
        print(f"The value at index {user_index} is {result}.")
    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except IndexError as ie:
        print(f"Error: {ie}")

