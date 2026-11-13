import sys

def find_largest_value(a, b):
    return max(a + b, a - b, a * b)

# Read input from standard input
a, b = map(int, sys.stdin.readline().split())

# Print the result
print(find_largest_value(a, b))