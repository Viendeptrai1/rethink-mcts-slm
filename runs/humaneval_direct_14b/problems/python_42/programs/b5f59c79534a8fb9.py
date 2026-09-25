def incr_list(l: list):
    """Return list with elements incremented by 1."""
    return [x + 1 for x in l]

# Test cases
print(incr_list([1, 2, 3]))  # Output: [2, 3, 4]
print(incr_list([5, 3, 5, 2, 3, 3, 9, 0, 123]))  # Output: [6, 4, 6, 3, 4, 4, 10, 1, 124]