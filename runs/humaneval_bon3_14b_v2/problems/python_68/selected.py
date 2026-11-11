def pluck(arr):
    if not arr:
        return []
    
    min_even_value = float('inf')
    min_index = -1
    
    for index, value in enumerate(arr):
        if value % 2 == 0 and value < min_even_value:
            min_even_value = value
            min_index = index
    
    if min_index == -1:
        return []
    
    return [min_even_value, min_index]