import sys

def is_odd_product(A, B):
    for C in range(1, 4):
        if (A * B * C) % 2 != 0:
            return "Yes"
    return "No"

# Read input from standard input
input_line = sys.stdin.readline().strip()
A, B = map(int, input_line.split())

# Call the function and print the result
print(is_odd_product(A, B))