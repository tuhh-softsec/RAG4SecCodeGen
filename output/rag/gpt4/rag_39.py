import random

# Function to safely convert a float to a string
def safe_float_to_str(value, max_length=10):
    # Convert the float to a string
    str_value = str(value)
    # Truncate the string to a maximum length to prevent buffer overflow
    if len(str_value) > max_length:
        str_value = str_value[:max_length]
    return str_value

# Generate three random floats
random_floats = [random.random() for _ in range(3)]

# Convert the floats to strings using the safe conversion function
str_a = safe_float_to_str(random_floats[0])
str_b = safe_float_to_str(random_floats[1])
str_c = safe_float_to_str(random_floats[2])

# Print the strings (for demonstration purposes)
print("str_a:", str_a)
print("str_b:", str_b)
print("str_c:", str_c)

