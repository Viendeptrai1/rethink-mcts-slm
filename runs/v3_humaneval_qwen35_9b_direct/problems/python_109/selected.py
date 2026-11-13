def move_one_ball(arr):
    if not arr:
        return True
    
    n = len(arr)
    # Count the number of times an element is greater than the next one
    # In a rotated sorted array, there should be at most one such drop
    drop_count = 0
    for i in range(n):
        if arr[i] > arr[(i + 1) % n]:
            drop_count += 1
    
    # If there is more than one drop, it's not a rotated sorted array
    return drop_count <= 1