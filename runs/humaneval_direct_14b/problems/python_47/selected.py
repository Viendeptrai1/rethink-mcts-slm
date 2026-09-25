def median(l: list):
    """Return median of elements in the list l."""
    if not l:
        raise ValueError("The list is empty")
    
    sorted_l = sorted(l)
    n = len(sorted_l)
    mid = n // 2
    
    if n % 2 == 0:
        return (sorted_l[mid - 1] + sorted_l[mid]) / 2
    else:
        return sorted_l[mid]