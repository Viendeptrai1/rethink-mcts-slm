def min_seconds_to_close_tabs(n, pos, l, r):
    # If the cursor is already within the desired segment, no action is needed
    if l <= pos <= r:
        return 0
    
    # Calculate the cost of moving the cursor to the leftmost tab in the desired segment
    move_to_left = abs(pos - l)
    
    # Calculate the cost of moving the cursor to the rightmost tab in the desired segment
    move_to_right = abs(pos - r)
    
    # Calculate the cost of closing all tabs to the left of the desired segment
    close_left = (l - 1) if l > 1 else 0
    
    # Calculate the cost of closing all tabs to the right of the desired segment
    close_right = (n - r) if r < n else 0
    
    # Calculate the cost of closing all tabs outside the desired segment by moving to the left
    cost_left = move_to_left + close_left
    
    # Calculate the cost of closing all tabs outside the desired segment by moving to the right
    cost_right = move_to_right + close_right
    
    # Calculate the cost of closing all tabs outside the desired segment by moving to the left and then to the right
    cost_left_then_right = move_to_left + close_left + (r - l + 1)
    
    # Calculate the cost of closing all tabs outside the desired segment by moving to the right and then to the left
    cost_right_then_left = move_to_right + close_right + (r - l + 1)
    
    # Return the minimum of all calculated costs
    return min(cost_left, cost_right, cost_left_then_right, cost_right_then_left)

# Read input
n, pos, l, r = map(int, input().split())

# Print the result
print(min_seconds_to_close_tabs(n, pos, l, r))