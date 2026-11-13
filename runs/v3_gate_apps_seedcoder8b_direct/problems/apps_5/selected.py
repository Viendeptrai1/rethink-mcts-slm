def min_seconds_to_close_tabs(n, pos, l, r):
    if l <= pos <= r:
        return 0
    
    # Calculate the number of tabs to the left and right of the segment
    tabs_to_left = max(0, pos - l)
    tabs_to_right = max(0, r - pos)
    
    # Calculate the number of tabs to close by moving left and right
    close_by_moving_left = tabs_to_left + (r - l + 1)
    close_by_moving_right = tabs_to_right + (r - l + 1)
    
    # Return the minimum of the two strategies
    return min(close_by_moving_left, close_by_moving_right)

# Read input
n, pos, l, r = map(int, input().split())

# Get the result
result = min_seconds_to_close_tabs(n, pos, l, r)

# Print the result
print(result)