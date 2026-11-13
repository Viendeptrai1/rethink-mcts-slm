def sort_array(array):
    if not array:
        return []
    
    sorted_array = array[:]
    if (sorted_array[0] + sorted_array[-1]) % 2 == 0:
        sorted_array.sort(reverse=True)
    else:
        sorted_array.sort()
    
    return sorted_array