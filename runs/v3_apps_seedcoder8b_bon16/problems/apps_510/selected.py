def minimum_duration(a, b, c, d):
    # Calculate initial pairwise distances
    dist_ab = abs(a - b)
    dist_bc = abs(b - c)
    dist_ac = abs(a - c)
    
    # Function to calculate the minimum time to increase distance to at least 'd'
    def min_time_to_increase(current_dist, target_dist):
        return max(0, target_dist - current_dist)
    
    # Calculate the minimum seconds needed for each pair
    time_ab = min_time_to_increase(dist_ab, d)
    time_bc = min_time_to_increase(dist_bc, d)
    time_ac = min_time_to_increase(dist_ac, d)
    
    # Since they can't move at the same time, we find the maximum time needed
    return max(time_ab, time_bc, time_ac)

# Read input from standard input
import sys
input = sys.stdin.read
data = input().strip()
a, b, c, d = map(int, data.split())

# Call the function and print the result
print(minimum_duration(a, b, c, d))