def get_value_from_sequence(id_sequence):
    # Define the maximum number of requests a user can make
    MAX_REQUESTS = 5
    request_count = 0

    # Define a mapping for expected input values if applicable
    # For example, if we expect inputs to be 'one', 'two', 'three', etc.
    # input_mapping = {'one': 0, 'two': 1, 'three': 2}
    # For simplicity, we'll assume numeric inputs are expected

    while request_count < MAX_REQUESTS:
        try:
            # Prompt the user for an index value
            user_input = input("Please enter an index value: ")

            # Validate the input is numeric
            index = int(user_input)

            # Check if the index is within the bounds of the id_sequence
            if index < 0 or index >= len(id_sequence):
                print("Error: Index is out of bounds.")
                continue

            # Increment the request count
            request_count += 1

            # Return the value at the index
            return id_sequence[index]

        except ValueError:
            # Handle non-numeric input
            print("Error: Please enter a valid numeric index.")
        except Exception as e:
            # Handle any other unexpected errors
            print(f"An unexpected error occurred: {e}")

    # If the user exceeds the maximum number of requests
    print("Error: You have exceeded the maximum number of requests.")
    return None

# Example usage:
# Define a sequence of IDs
id_sequence = [101, 202, 303, 404, 505]

# Call the function to get a value from the sequence
value = get_value_from_sequence(id_sequence)
if value is not None:
    print(f"The value at the given index is: {value}")

