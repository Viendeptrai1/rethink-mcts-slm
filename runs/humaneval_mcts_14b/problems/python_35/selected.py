def max_element(l: list):
    """Return maximum element in the list."""
    if not l:
        raise ValueError("The list is empty")
    
    max_value = l[0]
    for element in l:
        if element > max_value:
            max_value = element
    return max_value

# Test cases
print(max_element([1, 2, 3]))  # Output: 3
print(max_element([5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]))  # Output: 123