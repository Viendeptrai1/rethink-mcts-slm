def pluck(arr):
    if not arr:
        return []
    
    min_even_value = float('inf')
    min_index = -1
    
    for index, value in enumerate(arr):
        if value % 2 == 0 and value < min_even_value:
            min_even_value = value
            min_index = index
    
    if min_index == -1:
        return []
    
    return [min_even_value, min_index]

# Example usage:
# print(pluck([4, 2, 3]))  # Output: [2, 1]
# print(pluck([1, 2, 3]))  # Output: [2, 1]
# print(pluck([]))         # Output: []
# print(pluck([5, 0, 3, 0, 4, 2]))  # Output: [0, 1]