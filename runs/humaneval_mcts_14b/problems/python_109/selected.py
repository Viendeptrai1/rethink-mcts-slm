def move_one_ball(arr):
    if not arr:
        return True
    
    n = len(arr)
    inversion_count = 0
    inversion_point = -1
    
    for i in range(n):
        if arr[i] > arr[(i + 1) % n]:
            inversion_count += 1
            inversion_point = i
    
    if inversion_count == 0:
        return True
    elif inversion_count == 1:
        # Check if the array can be rotated to become sorted
        return arr[0] >= arr[-1]
    else:
        return False

# Test cases
print(move_one_ball([3, 4, 5, 1, 2]))  # True
print(move_one_ball([3, 5, 4, 1, 2]))  # False
print(move_one_ball([]))               # True
print(move_one_ball([1, 2, 3, 4, 5]))  # True
print(move_one_ball([2, 3, 4, 5, 1]))  # True
print(move_one_ball([5, 1, 2, 3, 4]))  # True
print(move_one_ball([1]))              # True