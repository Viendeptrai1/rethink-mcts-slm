def multiply(A, B):
    if 1 <= A <= 9 and 1 <= B <= 9:
        return A * B
    else:
        return -1

# Reading input from standard input
import sys
input = sys.stdin.read
data = input().split()
A = int(data[0])
B = int(data[1])

# Calling the function and printing the result
print(multiply(A, B))