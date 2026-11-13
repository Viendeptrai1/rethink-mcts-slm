def starts_one_ends(n):
    if n == 1:
        return 2
    start_with_1 = 10 ** (n - 1)
    end_with_1 = 9 * 10 ** (n - 2)
    both = 10 ** (n - 2)
    return start_with_1 + end_with_1 - both