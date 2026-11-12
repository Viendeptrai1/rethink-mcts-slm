def min_seconds_to_close_tabs(n, pos, l, r):
    # Distance to the left boundary
    left_distance = pos - l
    # Distance to the right boundary
    right_distance = r - pos
    
    # Total steps needed to reach the boundaries
    total_steps = left_distance + right_distance
    
    return total_steps

# Example usage:
# print(min_seconds_to_close_tabs(6, 3, 2, 4))  # Output: 5
# print(min_seconds_to_close_tabs(6, 3, 1, 3))  # Output: 1
# print(min_seconds_to_close_tabs(5, 2, 1, 5))  # Output: 0