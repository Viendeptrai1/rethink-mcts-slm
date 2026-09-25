def median(l: list):
    """Return median of elements in the list l."""
    if not l:
        raise ValueError("The list is empty")
    
    sorted_l = sorted(l)
    n = len(sorted_l)
    mid = n // 2
    
    if n % 2 == 1:
        return sorted_l[mid]
    else:
        return (sorted_l[mid - 1] + sorted_l[mid]) / 2

# Test cases
print(median([3, 1, 2, 4, 5]))  # Output: 3
print(median([-10, 4, 6, 1000, 10, 20]))  # Output: 15.0