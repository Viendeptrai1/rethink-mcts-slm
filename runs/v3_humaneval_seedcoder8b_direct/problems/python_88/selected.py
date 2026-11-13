def sort_array(array):
    if not array:
        return []
    
    if (array[0] + array[-1]) % 2 == 1:
        return sorted(array)
    else:
        return sorted(array, reverse=True)