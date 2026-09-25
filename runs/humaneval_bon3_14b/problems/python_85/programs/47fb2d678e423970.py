def add(lst):
    """Given a non-empty list of integers lst, add the even elements that are at odd indices."""
    result = 0
    for i in range(1, len(lst), 2):
        if lst[i] % 2 == 0:
            result += lst[i]
    return result

# Example usage:
# print(add([4, 2, 6, 7]))  # Output: 2