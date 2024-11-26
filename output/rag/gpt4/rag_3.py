import html

# Define a list of vehicles
vehicles = ["Car", "Truck", "Bicycle", "Motorcycle", "Boat"]

# Function to safely get an integer input from the user
def get_secure_integer_input(prompt, max_value):
    while True:
        try:
            user_input = input(prompt)
            index = int(user_input)
            if 0 <= index < max_value:
                return index
            else:
                print(f"Please enter a number between 0 and {max_value - 1}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Function to safely print a vehicle
def print_vehicle(vehicle):
    # Perform proper output encoding to prevent XSS attacks
    safe_vehicle = html.escape(vehicle)
    print(safe_vehicle)

# Prompt the user for the index of a vehicle and return that vehicle
index = get_secure_integer_input("Enter the index of the vehicle you want to see: ", len(vehicles))
selected_vehicle = vehicles[index]
print("You selected: ", end="")
print_vehicle(selected_vehicle)

# Loop through the array and print out each vehicle
print("\nList of all vehicles:")
for vehicle in vehicles:
    print_vehicle(vehicle)

