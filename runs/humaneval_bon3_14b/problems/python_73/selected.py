def smallest_change(arr):
    """
    Given an array arr of integers, find the minimum number of elements that
    need to be changed to make the array palindromic. A palindromic array is an array that
    is read the same backwards and forwards. In one change, you can change one element to any other element.
    """
    changes = 0
    left = 0
    right = len(arr) - 1
    
    while left < right:
        if arr[left] != arr[right]:
            changes += 1
        left += 1
        right -= 1
    
    return changes

# Example usage:
# print(smallest_change([1, 2, 3, 5, 4, 7, 9, 6]))  # Output: 4
# print(smallest_change([1, 2, 3, 4, 3, 2, 2]))    # Output: 1
# print(smallest_change([1, 2, 3, 2, 1]))          # Output: 0