def starts_one_ends(n):
    if n == 1:
        return 1  # Only the number 1 itself

    # Count numbers starting with 1
    start_with_1 = 9 * (10 ** (n - 2))

    # Count numbers ending with 1
    end_with_1 = 10 ** (n - 1)

    # Subtract the overlap where numbers both start and end with 1
    overlap = 9 * (10 ** (n - 3))

    return start_with_1 + end_with_1 - overlap