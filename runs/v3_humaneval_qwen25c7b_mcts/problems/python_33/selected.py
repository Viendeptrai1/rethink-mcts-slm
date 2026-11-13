def sort_third(l: list) -> list:
    indices_to_sort = [i for i in range(len(l)) if i % 3 == 0]
    sorted_values = sorted(l[i] for i in indices_to_sort)
    result = l[:]
    for original_index, new_value in zip(indices_to_sort, sorted_values):
        result[original_index] = new_value
    return result