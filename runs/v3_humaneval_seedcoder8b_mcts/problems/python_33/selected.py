def sort_third(l: list):
    result = l.copy()
    third_elements = [result[i] for i in range(0, len(result), 3)]
    third_elements.sort()
    
    for i, value in enumerate(third_elements):
        result[i * 3] = value
    
    return result