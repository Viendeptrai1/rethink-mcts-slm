import sys

# Read input from standard input
input_line = sys.stdin.read().strip()

# Convert the input string into a list of integers
numbers = list(map(int, input_line.split()))

# Find the smallest number in the list
smallest_number = min(numbers)

# Print the smallest number to standard output
print(smallest_number)