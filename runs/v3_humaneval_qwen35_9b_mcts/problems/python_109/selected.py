def move_one_ball(arr):
    if not arr:
        return True
    
    # Find the index of the minimum element
    min_index = 0
    for i in range(1, len(arr)):
        if arr[i] < arr[min_index]:
            min_index = i
    
    # Check if the array is sorted starting from min_index
    # We compare each element with the next one in the rotated sequence
    # The sequence is: arr[min_index], arr[min_index+1], ..., arr[n-1], arr[0], ..., arr[min_index-1]
    
    for i in range(len(arr) - 1):
        current_idx = (min_index + i) % len(arr)
        next_idx = (min_index + i + 1) % len(arr)
        
        if arr[current_idx] > arr[next_idx]:
            return False
    
    return True