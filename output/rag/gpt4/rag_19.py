import random
import html

def generate_secure_random_number():
    try:
        # Generate a random number larger than 1000
        random_number = random.randint(1001, 9999)
        
        # Perform proper output encoding to prevent potential output-related vulnerabilities
        safe_output = html.escape(str(random_number))
        
        # Print the securely encoded number
        print(safe_output)
        
    except Exception as e:
        # Print a generic error message without unnecessary details
        print("An error occurred while generating the random number.")

# Call the function to generate and print the random number
generate_secure_random_number()

