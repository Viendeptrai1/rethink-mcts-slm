def next_smallest(lst):
    unique_elements = sorted(set(lst))
    return unique_elements[1] if len(unique_elements) > 1 else None