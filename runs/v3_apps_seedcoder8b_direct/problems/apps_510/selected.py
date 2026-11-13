def min_duration(a, b, c, d):
    # Calculate the initial pairwise distances
    dist_ab = abs(a - b)
    dist_bc = abs(b - c)
    dist_ac = abs(a - c)
    
    # If all distances are already greater than or equal to d, no time is needed
    if dist_ab >= d and dist_bc >= d and dist_ac >= d:
        return 0
    
    # Calculate the maximum distance that needs to be covered
    max_distance = max(dist_ab, dist_bc, dist_ac)
    
    # The minimum time required is the difference between the maximum distance
    # and the required minimum distance d, divided by 2 (since only one can move at a time)
    return (max_distance - d + 1) // 2

# Read input
a, b, c, d = map(int, input().split())

# Calculate and print the result
print(min_duration(a, b, c, d))