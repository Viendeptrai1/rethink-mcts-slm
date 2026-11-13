def starts_one_ends(n):
    if n == 1:
        return 2  # Only numbers 1 and 9 start or end with 1
    else:
        return 9 * (10 ** (n - 2)) + 9  # Numbers starting with 1 and ending with 1