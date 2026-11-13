def sort_even(l: list):
    even_indices = sorted([(i, l[i]) for i in range(0, len(l), 2)], key=lambda x: x[1])
    result = l.copy()
    for i, (index, value) in enumerate(even_indices):
        result[index] = value
    return result