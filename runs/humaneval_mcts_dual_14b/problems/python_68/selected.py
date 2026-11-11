def pluck(arr):
    smallest_even = float('inf')
    smallest_index = -1
    
    for index, value in enumerate(arr):
        if value % 2 == 0 and value < smallest_even:
            smallest_even = value
            smallest_index = index
    
    if smallest_index == -1:
        return []
    else:
        return [smallest_even, smallest_index]