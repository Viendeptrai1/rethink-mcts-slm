def starts_one_ends(n):
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
    if n == 1:
        return 1  # Only the number 1 itself

    # Count numbers starting with 1
    start_with_1 = 9 * (10 ** (n - 2))

    # Count numbers ending with 1
    end_with_1 = 10 ** (n - 1)

    # Count numbers both starting and ending with 1
    both_start_and_end_with_1 = 9 * (10 ** (n - 3))

    # Total count is the sum of numbers starting with 1 and ending with 1,
    # minus those counted twice (both starting and ending with 1)
    total_count = start_with_1 + end_with_1 - both_start_and_end_with_1

    return total_count