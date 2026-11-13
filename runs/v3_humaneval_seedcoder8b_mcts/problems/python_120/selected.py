def maximum(arr, k):
    if k == 0:
        return []
    
    sorted_arr = sorted(arr, reverse=True)
    return sorted(sorted_arr[:k])