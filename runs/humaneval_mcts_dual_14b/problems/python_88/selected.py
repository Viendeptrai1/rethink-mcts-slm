def sort_array(array):
    if not array:
        return []

    sum_first_last = array[0] + array[-1]
    if sum_first_last % 2 == 0:
        return sorted(array, reverse=True)
    else:
        return sorted(array)

# Example usage:
# print(sort_array([]))  # Output: []
# print(sort_array([5]))  # Output: [5]
# print(sort_array([2, 4, 3, 0, 1, 5]))  # Output: [0, 1, 2, 3, 4, 5]
# print(sort_array([2, 4, 3, 0, 1, 5, 6]))  # Output: [6, 5, 4, 3, 2, 1, 0]