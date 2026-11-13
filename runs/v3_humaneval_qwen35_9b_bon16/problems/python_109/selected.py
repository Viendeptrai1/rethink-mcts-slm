def move_one_ball(arr):
    """
    Determines if the array can be sorted in non-decreasing order by performing
    right shift operations any number of times.
    
    The problem is equivalent to checking if the array has at most one "descent"
    (a place where arr[i] > arr[i+1]). If there is exactly one descent, the array
    is a rotated sorted array. If there are zero descents, it's already sorted.
    If there are two or more descents, it cannot be sorted by rotation.
    
    Edge case: Empty array or single element array is considered sorted.
    """
    if len(arr) <= 1:
        return True
    
    descents = 0
    n = len(arr)
    
    for i in range(n):
        if arr[i] > arr[(i + 1) % n]:
            descents += 1
            if descents > 1:
                return False
    
    # If we found exactly 1 descent, it means the array is a rotated sorted array.
    # If we found 0 descents, it means the array is already sorted.
    # In both cases, we can achieve sorted order by rotating.
    return True