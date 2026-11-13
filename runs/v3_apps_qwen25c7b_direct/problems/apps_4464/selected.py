def can_make_sum_congruent(A, B, C):
    return "YES" if (C % A == 0) else "NO"

# Read input from standard input
import sys
input = sys.stdin.read
data = input().split()

# Parse the input
A = int(data[0])
B = int(data[1])
C = int(data[2])

# Call the function and print the result
print(can_make_sum_congruent(A, B, C))