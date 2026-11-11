import sys

def min_performance_duration(a, b, c, d):
    # Sort the positions to simplify the calculation
    x, y, z = sorted([a, b, c])
    
    # Calculate the required distances
    dist1 = max(0, d - (y - x))
    dist2 = max(0, d - (z - y))
    
    # The total time needed is the sum of the required distances
    return dist1 + dist2

# Read input
input = sys.stdin.read
data = input().split()
a = int(data[0])
b = int(data[1])
c = int(data[2])
d = int(data[3])

# Calculate and print the result
result = min_performance_duration(a, b, c, d)
print(result)