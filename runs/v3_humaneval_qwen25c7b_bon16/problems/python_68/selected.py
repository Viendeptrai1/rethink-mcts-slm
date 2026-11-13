def pluck(arr):
    min_even_value = float('inf')
    min_index = -1

    for i, value in enumerate(arr):
        if value % 2 == 0 and value < min_even_value:
            min_even_value = value
            min_index = i

    return [min_even_value, min_index] if min_index != -1 else []