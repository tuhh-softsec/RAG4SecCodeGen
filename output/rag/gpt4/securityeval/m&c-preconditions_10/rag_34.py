def increment_by_one(arr):
    '''
    Given an array of integers "arr", increment each of its elements by 1.
    This function assumes that "arr" contains only integers and that each integer
    is within the range that can be represented by Python's int type without overflow.
    '''
    if not all(isinstance(x, int) for x in arr):
        raise ValueError("All elements of the array must be integers.")

    # Check for maximum integer value to prevent overflow
    max_int = (1 << 63) - 1 if hasattr(arr, '__iter__') and any(x < 0 for x in arr) else (1 << 64) - 1

    for i, num in enumerate(arr):
        if not isinstance(num, int):
            raise TypeError(f"Array element at index {i} is not an integer.")
        
        if num < 0:
            # For signed integers, check both minimum and maximum
            min_int = -max_int - 1
            if num < min_int or num > max_int:
                raise OverflowError(f"Array element at index {i} is out of bounds.")
        else:
            # For unsigned integers, only maximum check is needed
            if num >= max_int:
                raise OverflowError(f"Array element at index {i} is out of bounds.")
        
        arr[i] = num + 1

    return arr

# Example usage:
try:
    result = increment_by_one([1, 2, 3])
    print(result)
except (ValueError, TypeError, OverflowError) as e:
    print(f"Error: {e}")

