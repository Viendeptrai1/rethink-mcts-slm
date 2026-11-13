import sys

def check_odd_product(A, B):
    # Check if either A or B is odd
    if A % 2 != 0 or B % 2 != 0:
        return "Yes"
    else:
        return "No"

# Read input from standard input
input_line = sys.stdin.readline().strip()
A, B = map(int, input_line.split())

# Determine if there exists an integer C such that A * B * C is odd
result = check_odd_product(A, B)
print(result)