def sort_third(l: list):
    third_elements = sorted(l[2::3])
    result = l.copy()
    result[2::3] = third_elements
    return result