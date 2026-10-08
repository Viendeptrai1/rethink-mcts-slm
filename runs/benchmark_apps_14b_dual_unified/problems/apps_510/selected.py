import sys

def min_performance_duration(a, b, c, d):
    # Sort the initial positions to simplify calculations
    x, y, z = sorted([a, b, c])
    
    # Calculate the required distances between the ropewalkers
    dist_xy = max(0, d - (y - x))
    dist_yz = max(0, d - (z - y))
    
    # The total time required is the sum of the required distances
    return dist_xy + dist_yz

# Read input from stdin
input = sys.stdin.read
data = input().split()

# Parse the input values
a = int(data[0])
b = int(data[1])
c = int(data[2])
d = int(data[3])

# Calculate and print the result
result = min_performance_duration(a, b, c, d)
print(result)