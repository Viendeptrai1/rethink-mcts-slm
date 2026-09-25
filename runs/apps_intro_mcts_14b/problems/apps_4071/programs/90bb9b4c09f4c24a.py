import sys

# Read input from standard input
a = int(sys.stdin.read().strip())

# Check if the input integer a is within the valid range
if 1 <= a <= 30:
    # Calculate 3 raised to the power of a
    result = 3 ** a
    # Print the result to standard output
    print(result)
else:
    # If the input is out of range, print an error message or handle it as needed
    print("Error: Input is out of the valid range.")