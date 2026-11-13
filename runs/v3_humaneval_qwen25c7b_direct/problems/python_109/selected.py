def move_one_ball(arr):
    if not arr:
        return True
    
    n = len(arr)
    count = 0
    
    for i in range(1, n):
        if arr[i] < arr[i - 1]:
            count += 1
            start = i
    
    if arr[0] < arr[-1]:
        count += 1
    
    return count <= 1