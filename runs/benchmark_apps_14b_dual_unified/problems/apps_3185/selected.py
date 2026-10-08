import math

def find_n_for_factorial(factorial_value):
    # Convert the input string to an integer
    factorial_value = int(factorial_value)
    
    # Initial guess for n
    n = 1
    
    # Increase n until factorial(n) is greater than or equal to the given factorial value
    while math.factorial(n) < factorial_value:
        n += 1
    
    # If factorial(n) is exactly equal to the given factorial value, return n
    if math.factorial(n) == factorial_value:
        return n
    
    # Otherwise, decrement n to find the exact value
    return n - 1

# Read input from standard input
factorial_input = input().strip()

# Find and print the value of n
print(find_n_for_factorial(factorial_input))