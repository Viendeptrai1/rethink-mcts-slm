import sys

def min_fare(A, B, C, D):
    return min(B, A) + min(D, C)

# Read input from stdin
input = sys.stdin.read
data = input().split()

# Convert input data to integers
A = int(data[0])
B = int(data[1])
C = int(data[2])
D = int(data[3])

# Calculate and print the minimum total fare
print(min_fare(A, B, C, D))