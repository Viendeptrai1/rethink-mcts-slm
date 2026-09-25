import sys

def max_product(a, b, c, d):
    # Calculate the product of the maximum values within the ranges
    return max(a * c, a * d, b * c, b * d)

# Read input from standard input
input_line = sys.stdin.read().strip()
a, b, c, d = map(int, input_line.split())

# Calculate and print the maximum product
print(max_product(a, b, c, d))