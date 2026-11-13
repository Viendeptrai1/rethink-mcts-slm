def sort_even(l: list):
    even_indices = sorted([(i, val) for i, val in enumerate(l) if i % 2 == 0], key=lambda x: x[1])
    result = l.copy()
    for (i, val), (_, sorted_val) in zip([(i, val) for i, val in enumerate(l) if i % 2 == 0], even_indices):
        result[i] = sorted_val
    return result