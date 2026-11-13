def sort_even(l: list):
    even_indices_values = [l[i] for i in range(0, len(l), 2)]
    even_indices_values.sort()
    result = l[:]
    for i, value in enumerate(even_indices_values):
        result[2 * i] = value
    return result