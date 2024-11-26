import random
import sys

# Function to generate a random integer larger than 1000
def generate_large_random_int():
    return random.randint(1001, sys.maxsize)

# Function to add three integers with overflow check
def safe_add(a, b, c):
    # Check for potential overflow
    max_val = sys.maxsize
    if a > max_val - b or a > max_val - c or b > max_val - c or a + b > max_val - c:
        raise OverflowError("Integer addition overflow")
    return a + b + c

# Main function to generate three integers and print their sum
def main():
    try:
        # Generate three random integers larger than 1000
        a = generate_large_random_int()
        b = generate_large_random_int()
        c = generate_large_random_int()

        # Print the three integers
        print(f"a : {a}")
        print(f"b : {b}")
        print(f"c : {c}")

        # Add the three integers and print the result
        sum_of_integers = safe_add(a, b, c)
        print(f"sum: {sum_of_integers}")
        print(f"sum2: {sum_of_integers}")

    except OverflowError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

