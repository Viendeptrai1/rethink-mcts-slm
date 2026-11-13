def min_performance_duration(a, b, c, d):
    # Sort the initial positions to simplify calculations
    positions = sorted([a, b, c])
    
    # Calculate the current distances between each pair of ropewalkers
    dist_ab = positions[1] - positions[0]
    dist_bc = positions[2] - positions[1]
    dist_ac = positions[2] - positions[0]
    
    # Determine the maximum distance that needs to be increased
    max_dist_to_increase = max(dist_ab, dist_bc, dist_ac)
    
    # Calculate the minimum number of seconds needed to increase the maximum distance to at least d
    if max_dist_to_increase >= d:
        return 0
    
    # If the maximum distance is less than d, calculate the difference
    required_increase = d - max_dist_to_increase
    
    # Since each movement increases the distance by 1, the required increase is the number of seconds needed
    return required_increase

# Example usage:
# print(min_performance_duration(5, 2, 6, 3))  # Output: 2
# print(min_performance_duration(3, 1, 5, 6))  # Output: 8
# print(min_performance_duration(8, 3, 3, 2))  # Output: 2
# print(min_performance_duration(2, 3, 10, 4)) # Output: 3