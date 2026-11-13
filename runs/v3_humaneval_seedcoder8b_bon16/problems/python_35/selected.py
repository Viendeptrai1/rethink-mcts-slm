def max_element(l: list):
    if not l:
        raise ValueError("Cannot find maximum of an empty list")
    return max(l)