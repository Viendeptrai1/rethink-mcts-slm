def sort_array(array):
    if not array:
        return []

    first_value = array[0]
    last_value = array[-1]
    sum_values = first_value + last_value

    if sum_values % 2 == 0:
        return sorted(array, reverse=True)
    else:
        return sorted(array)