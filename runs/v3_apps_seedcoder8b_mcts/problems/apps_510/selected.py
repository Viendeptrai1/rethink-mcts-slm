def min_duration(a, b, c, d):
    # Calculate the initial distances between each pair of ropewalkers
    dist_ab = abs(a - b)
    dist_bc = abs(b - c)
    dist_ac = abs(a - c)
    
    # Calculate the required minimum distances
    min_dist_ab = d
    min_dist_bc = d
    min_dist_ac = d
    
    # Calculate the additional distance needed to satisfy the conditions
    additional_dist_ab = max(0, min_dist_ab - dist_ab)
    additional_dist_bc = max(0, min_dist_bc - dist_bc)
    additional_dist_ac = max(0, min_dist_ac - dist_ac)
    
    # The total additional distance needed is the maximum of the three
    total_additional_dist = max(additional_dist_ab, additional_dist_bc, additional_dist_ac)
    
    # The minimum duration is the total additional distance needed
    return total_additional_dist

# Read input
a, b, c, d = map(int, input().split())

# Calculate and print the result
print(min_duration(a, b, c, d))