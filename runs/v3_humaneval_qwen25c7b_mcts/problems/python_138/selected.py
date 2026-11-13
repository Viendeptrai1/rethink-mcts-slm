def is_equal_to_sum_even(n):
    if n < 8:
        return False
    return (n - 8) % 2 == 0