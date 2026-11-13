def sort_even(l: list) -> list:
    even_indices_values = sorted(l[i] for i in range(0, len(l), 2))
    result = l[:]
    even_index = 0
    for i in range(0, len(result), 2):
        result[i] = even_indices_values[even_index]
        even_index += 1
    return result