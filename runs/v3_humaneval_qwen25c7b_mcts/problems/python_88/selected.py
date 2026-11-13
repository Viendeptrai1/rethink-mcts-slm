def sort_array(array):
    if not array:
        return []
    
    if len(array) == 1:
        return array[:]
    
    if (array[0] + array[-1]) % 2 == 0:
        return sorted(array, reverse=True)
    else:
        return sorted(array)