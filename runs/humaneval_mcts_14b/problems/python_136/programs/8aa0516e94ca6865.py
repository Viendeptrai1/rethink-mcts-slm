def largest_smallest_integers(lst):
    largest_negative = None
    smallest_positive = None

    for num in lst:
        if num < 0:
            if largest_negative is None or num > largest_negative:
                largest_negative = num
        elif num > 0:
            if smallest_positive is None or num < smallest_positive:
                smallest_positive = num

    return (largest_negative, smallest_positive)

# Test cases
print(largest_smallest_integers([2, 4, 1, 3, 5, 7]))  # Output: (None, 1)
print(largest_smallest_integers([]))                  # Output: (None, None)
print(largest_smallest_integers([0]))                 # Output: (None, None)
print(largest_smallest_integers([-3, -1, -4, 2, 5]))  # Output: (-1, 2)
print(largest_smallest_integers([-10, -20, 0, 10, 20]))  # Output: (-10, 10)