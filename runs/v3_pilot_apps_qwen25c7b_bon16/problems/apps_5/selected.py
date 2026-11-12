def min_seconds_to_close_tabs(n, pos, l, r):
    # Calculate the number of seconds needed to move the cursor to the start of the segment
    seconds = abs(pos - l)
    # Add the time to close all tabs to the left of the segment
    seconds += l - 1
    # Add the time to move the cursor to the end of the segment
    seconds += r - pos
    # Add the time to close all tabs to the right of the segment
    seconds += n - r
    return seconds

# Input reading
n, pos, l, r = map(int, input().split())

# Output the result
print(min_seconds_to_close_tabs(n, pos, l, r))