def sum_squares(lst):
    total_sum = 0
    for index, value in enumerate(lst):
        if index % 3 == 0:
            total_sum += value ** 2
        elif index % 4 == 0:
            total_sum += value ** 3
        else:
            total_sum += value
    return total_sum

# Test cases
print(sum_squares([1, 2, 3]))  # Output: 6
print(sum_squares([]))         # Output: 0
print(sum_squares([-1, -5, 2, -1, -5]))  # Output: -126