def sort_third(l: list):
    if not l:
        return l
    
    # Extract elements at indices divisible by 3 (0-based)
    indices_to_sort = [i for i in range(0, len(l), 3)]
    values_to_sort = [l[i] for i in indices_to_sort]
    
    # Sort the extracted values
    values_to_sort.sort()
    
    # Place sorted values back into the original list at the specified indices
    for i, idx in enumerate(indices_to_sort):
        l[idx] = values_to_sort[i]
    
    return l