def min_fare(A, B, C, D):
    min_train_fare = min(A, B)
    min_bus_fare = min(C, D)
    return min_train_fare + min_bus_fare

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
A = int(data[0])
B = int(data[1])
C = int(data[2])
D = int(data[3])

# Calculate and print result
print(min_fare(A, B, C, D))