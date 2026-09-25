def pluck(arr):
    if not arr:
        return []
    
    smallest_even = float('inf')
    smallest_index = -1
    
    for index, value in enumerate(arr):
        if value % 2 == 0 and value < smallest_even:
            smallest_even = value
            smallest_index = index
    
    if smallest_index == -1:
        return []
    
    return [smallest_even, smallest_index]

# Example usage:
# print(pluck([4, 2, 3]))  # Output: [2, 1]
# print(pluck([1, 2, 3]))  # Output: [2, 1]
# print(pluck([]))         # Output: []
# print(pluck([5, 0, 3, 0, 4, 2]))  # Output: [0, 1]