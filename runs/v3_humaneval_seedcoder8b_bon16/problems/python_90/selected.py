def next_smallest(lst):
    if len(lst) < 2:
        return None
    unique_elements = sorted(set(lst))
    if len(unique_elements) < 2:
        return None
    return unique_elements[1]