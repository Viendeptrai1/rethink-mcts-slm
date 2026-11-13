def remaining_water(A, B, C):
    transfer = min(B, A - B)
    return C - transfer

# Read input from standard input
import sys
input = sys.stdin.read
data = input().split()

# Parse the input
A = int(data[0])
B = int(data[1])
C = int(data[2])

# Calculate the remaining water in Bottle 2
result = remaining_water(A, B, C)

# Print the result
print(result)