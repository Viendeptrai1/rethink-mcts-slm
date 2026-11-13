def min_total_distance(N, K, x):
    # Initialize the minimum distance to a large number
    min_distance = float('inf')
    
    # Iterate over all possible combinations of activating N type-A robots and N type-B robots
    from itertools import combinations
    
    for A_robots in combinations(range(N), N):
        total_distance = 0
        for a in A_robots:
            # Calculate distance for type-A robot
            total_distance += (x[a] - 0) * 2
        
        # Remaining robots are type-B robots
        B_robots = [i for i in range(N) if i not in A_robots]
        for b in B_robots:
            # Calculate distance for type-B robot
            total_distance += (K - x[b]) * 2
        
        # Update the minimum distance found
        min_distance = min(min_distance, total_distance)
    
    return min_distance

# Read input
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
K = int(data[1])
x = list(map(int, data[2:]))

# Calculate and print the minimum possible total distance
print(min_total_distance(N, K, x))