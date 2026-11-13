def maximum(arr, k):
    if k == 0:
        return []
    sorted_arr = sorted(arr)
    return sorted_arr[-k:]