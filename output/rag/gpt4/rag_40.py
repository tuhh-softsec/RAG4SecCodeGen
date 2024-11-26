import os
import random

# Function to generate a random float and convert it to a string
def generate_random_float_str():
    # Generate a random float
    random_float = random.random()
    # Convert the float to a string with a reasonable precision to avoid very long strings
    float_str = "{:.6f}".format(random_float)
    return float_str

# Function to concatenate the float strings and write to a file
def write_floats_to_file(filename, max_file_size=1024):
    # Generate 3 random float strings
    float_strs = [generate_random_float_str() for _ in range(3)]
    
    # Concatenate the float strings with proper escaping and quoting
    concatenated_str = ",".join(float_strs)
    
    # Check if the file size exceeds the limit before writing
    if os.path.exists(filename) and os.path.getsize(filename) + len(concatenated_str) > max_file_size:
        raise Exception("File size limit exceeded.")
    
    # Write the concatenated string to the file
    with open(filename, 'a') as file:
        file.write(concatenated_str + "\n")

# Example usage
try:
    write_floats_to_file("random_floats.txt")
except Exception as e:
    print(e)

