def sort_array(array):
    if not array:
        return []

    first_value = array[0]
    last_value = array[-1]
    sum_values = first_value + last_value

    if sum_values % 2 == 0:
        # Sort in descending order
        return sorted(array, reverse=True)
    else:
        # Sort in ascending order
        return sorted(array)

# Test cases
print(sort_array([]))  # Output: []
print(sort_array([5]))  # Output: [5]
print(sort_array([2, 4, 3, 0, 1, 5]))  # Output: [0, 1, 2, 3, 4, 5]
print(sort_array([2, 4, 3, 0, 1, 5, 6]))  # Output: [6, 5, 4, 3, 2, 1, 0]