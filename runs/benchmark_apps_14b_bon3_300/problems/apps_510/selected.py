import sys

def min_performance_duration(a, b, c, d):
    # Calculate the initial distances between each pair of ropewalkers
    dist_ab = abs(a - b)
    dist_bc = abs(b - c)
    dist_ca = abs(c - a)
    
    # If all distances are already at least d, the performance is already done
    if dist_ab >= d and dist_bc >= d and dist_ca >= d:
        return 0
    
    # Calculate the minimum number of moves needed for each pair
    moves_ab = max(0, d - dist_ab)
    moves_bc = max(0, d - dist_bc)
    moves_ca = max(0, d - dist_ca)
    
    # The total minimum duration is the sum of the maximum moves needed for each pair
    return moves_ab + moves_bc + moves_ca

# Read input from stdin
input = sys.stdin.read().strip().split()
a = int(input[0])
b = int(input[1])
c = int(input[2])
d = int(input[3])

# Calculate and print the result
result = min_performance_duration(a, b, c, d)
print(result)