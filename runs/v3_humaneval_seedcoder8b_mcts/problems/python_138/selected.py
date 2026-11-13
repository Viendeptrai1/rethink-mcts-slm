def is_equal_to_sum_even(n):
    if n % 4 != 0:
        return False
    return n // 4 % 2 == 0