import sys

def check_odd_product(A, B):
    # Check if both A and B are odd
    if A % 2 == 1 and B % 2 == 1:
        return "Yes"
    else:
        return "No"

# Read input
A, B = map(int, sys.stdin.readline().split())

# Print the result
print(check_odd_product(A, B))