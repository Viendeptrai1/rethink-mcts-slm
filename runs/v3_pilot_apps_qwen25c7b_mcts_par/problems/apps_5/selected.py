def min_seconds_to_close_tabs(n, pos, l, r):
    return min(pos - l, r - pos)

# Example usage:
# print(min_seconds_to_close_tabs(6, 3, 2, 4))  # Output: 5
# print(min_seconds_to_close_tabs(6, 3, 1, 3))  # Output: 1
# print(min_seconds_to_close_tabs(5, 2, 1, 5))  # Output: 0