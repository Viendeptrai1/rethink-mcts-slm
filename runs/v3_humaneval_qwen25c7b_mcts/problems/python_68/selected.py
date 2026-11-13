def pluck(arr):
    smallest_even = float('inf')
    index_of_smallest_even = -1

    for i, num in enumerate(arr):
        if num % 2 == 0 and num < smallest_even:
            smallest_even = num
            index_of_smallest_even = i

    if smallest_even == float('inf'):
        return []

    return [smallest_even, index_of_smallest_even]