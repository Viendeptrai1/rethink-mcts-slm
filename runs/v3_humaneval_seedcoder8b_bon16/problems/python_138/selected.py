def is_equal_to_sum_even(n):
    if n < 8:
        return False
    if n % 2 != 0:
        return False
    return n % 2 == 0 and n >= 8