def sort_third(l: list):
    if not l:
        return l
    
    # Extract elements at indices divisible by 3 (0-indexed)
    third_elements = [l[i] for i in range(0, len(l), 3)]
    
    # Sort those elements
    third_elements.sort()
    
    # Reconstruct the list
    result = l.copy()
    idx = 0
    for i in range(0, len(l), 3):
        result[i] = third_elements[idx]
        idx += 1
    
    return result