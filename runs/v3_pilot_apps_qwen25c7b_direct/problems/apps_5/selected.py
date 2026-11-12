def min_seconds_to_close_tabs(n, pos, l, r):
    # Calculate the number of seconds needed to move the cursor to the leftmost tab in the range [l, r]
    left_moves = max(0, l - pos)
    # Calculate the number of seconds needed to move the cursor to the rightmost tab in the range [l, r]
    right_moves = max(0, pos - r)
    # Calculate the total number of seconds needed to close all tabs outside the range [l, r]
    return left_moves + right_moves

# Example usage:
# Input
n = 6
pos = 3
l = 2
r = 4
# Output
print(min_seconds_to_close_tabs(n, pos, l, r))  # Output: 5

n = 6
pos = 3
l = 1
r = 3
# Output
print(min_seconds_to_close_tabs(n, pos, l, r))  # Output: 1

n = 5
pos = 2
l = 1
r = 5
# Output
print(min_seconds_to_close_tabs(n, pos, l, r))  # Output: 0