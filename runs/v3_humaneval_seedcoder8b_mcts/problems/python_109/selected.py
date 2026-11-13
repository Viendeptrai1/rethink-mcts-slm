def move_one_ball(arr):
    if not arr:
        return True
    
    n = len(arr)
    min_idx = arr.index(min(arr))
    
    rotated = arr[min_idx:] + arr[:min_idx]
    
    for i in range(1, n):
        if rotated[i] < rotated[i-1]:
            return False
    
    return True