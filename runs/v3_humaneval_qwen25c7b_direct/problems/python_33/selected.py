def sort_third(l: list) -> list:
    indices_divisible_by_three = [i for i in range(len(l)) if i % 3 == 0]
    values_at_divisible_indices = [l[i] for i in indices_divisible_by_three]
    sorted_values = sorted(values_at_divisible_indices)
    
    result = l[:]
    for original_index, new_value in zip(indices_divisible_by_three, sorted_values):
        result[original_index] = new_value
    
    return result