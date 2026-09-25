def move_one_ball(arr):
    if not arr:
        return True
    
    n = len(arr)
    count = 0
    
    for i in range(1, n):
        if arr[i] < arr[i - 1]:
            count += 1
    
    if arr[n - 1] > arr[0]:
        count += 1
    
    return count <= 1

# Test cases
print(move_one_ball([3, 4, 5, 1, 2]))  # True
print(move_one_ball([3, 5, 4, 1, 2]))  # False
print(move_one_ball([]))               # True
print(move_one_ball([1, 2, 3, 4, 5]))  # True
print(move_one_ball([2, 3, 4, 5, 1]))  # True
print(move_one_ball([5, 1, 2, 3, 4]))  # True
print(move_one_ball([4, 5, 1, 2, 3]))  # True
print(move_one_ball([1]))              # True