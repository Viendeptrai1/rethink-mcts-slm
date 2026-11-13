def median(l: list):
    """Return median of elements in the list l."""
    n = len(l)
    if n == 0:
        return None
    sorted_l = sorted(l)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_l[mid - 1] + sorted_l[mid]) / 2
    else:
        return sorted_l[mid]