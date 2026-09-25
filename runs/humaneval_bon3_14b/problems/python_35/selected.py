def max_element(l: list):
    """Return maximum element in the list."""
    if not l:
        raise ValueError("The list is empty")
    return max(l)