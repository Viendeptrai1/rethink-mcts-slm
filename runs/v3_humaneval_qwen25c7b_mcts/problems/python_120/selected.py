def maximum(arr, k):
    if k == 0:
        return []
    elif k >= len(arr):
        return sorted(arr)
    else:
        return sorted(arr)[-k:]