def sort_even(l: list) -> list:
    even_indices = [i for i in range(len(l)) if i % 2 == 0]
    even_values = sorted([l[i] for i in even_indices])
    result = l[:]
    for i, value in zip(even_indices, even_values):
        result[i] = value
    return result