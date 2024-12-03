from typing import List

MAX_LIST_SIZE = 10000  # Define a maximum allowed list size to prevent resource exhaustion

class ListSizeError(Exception):
    """Custom exception for list size errors."""
    pass

def increment_by_one(arr: List[int]) -> List[int]:
    '''
    Given an array of integers "arr", increment each of its elements by 1.
    
    :param arr: List of integers to be incremented.
    :return: A new list with each element incremented by 1.
    :raises TypeError: If the input is not a list or contains non-integer elements.
    :raises ListSizeError: If the list exceeds the maximum allowed size.
    '''
    # Check if the input is a list
    if not isinstance(arr, list):
        raise TypeError("Input must be a list.")
    
    # Check for maximum allowed list size to prevent resource exhaustion
    if len(arr) > MAX_LIST_SIZE:
        raise ListSizeError(f"List size exceeds the maximum allowed limit of {MAX_LIST_SIZE}.")

    # Check if all elements in the list are integers
    if not all(isinstance(item, int) for item in arr):
        raise TypeError("All elements in the array must be integers.")
    
    # Increment each element by one and return the new list
    return [item + 1 for item in arr]

# Example usage:
try:
    original_array = [1, 2, 3, 4, 5]
    incremented_array = increment_by_one(original_array)
    print("Original array:", original_array)
    print("Incremented array:", incremented_array)
except (TypeError, ListSizeError) as e:
    print("Error:", e)

