def sort_even(l: list):
    even_indices = [i for i in range(0, len(l), 2)]
    even_values = sorted(l[i] for i in even_indices)
    
    for i, value in zip(even_indices, even_values):
        l[i] = value
    
    return l