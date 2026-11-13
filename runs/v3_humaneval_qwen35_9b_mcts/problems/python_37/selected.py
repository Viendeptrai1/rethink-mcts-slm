def sort_even(l: list):
    even_indices = [i for i in range(0, len(l), 2)]
    even_values = [l[i] for i in even_indices]
    even_values.sort()
    
    result = l.copy()
    for i, idx in enumerate(even_indices):
        result[idx] = even_values[i]
    
    return result