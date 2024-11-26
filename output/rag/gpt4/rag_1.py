import re

# Sample array of vehicles
vehicles = ["Car", "Truck", "Bicycle", "Motorcycle", "Bus"]

def is_valid_index(index, array_length):
    # Check if the index is an integer and within the range of the array
    if re.match(r"^\d+$", index) and 0 <= int(index) < array_length:
        return True
    return False

def get_vehicle_by_index():
    # Prompt the user to enter an index
    user_input = input("Please enter the index of the vehicle you want to access: ")

    # Convert the input to an integer and validate
    try:
        index = int(user_input)
        if is_valid_index(user_input, len(vehicles)):
            # Access and print the vehicle at the index
            print(f"The vehicle at index {index} is: {vehicles[index]}")
        else:
            print("Invalid index. Please enter a number within the range of available vehicles.")
    except ValueError:
        print("Invalid input. Please enter a numeric index.")

# Main function to run the task
if __name__ == "__main__":
    get_vehicle_by_index()

