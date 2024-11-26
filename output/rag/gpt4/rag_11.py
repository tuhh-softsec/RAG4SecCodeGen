# Define the array of ID sequences
id_sequence = [1001, 1002, 1003, 1004, 1005]  # Example array

# Define a function to get the value at a given index from id_sequence
def get_value_at_index():
    # Prompt the user for an index value
    try:
        index = int(input("Please enter the index value: "))
    except ValueError:
        print("Invalid input: Index must be an integer.")
        return None

    # Validate the index (Guideline #2 and #4)
    if index < 0 or index >= len(id_sequence):
        print("Invalid input: Index is out of bounds.")
        return None

    # Retrieve and return the value at the index (Guideline #1)
    value = id_sequence[index]
    return value

# Example usage of the function
if __name__ == "__main__":
    # Implement a request limit (Guideline #5)
    MAX_REQUESTS = 3
    request_count = 0

    while request_count < MAX_REQUESTS:
        result = get_value_at_index()
        if result is not None:
            print(f"The value at the provided index is: {result}")
            break
        request_count += 1

    if request_count >= MAX_REQUESTS:
        print("Request limit exceeded. Please try again later.")

