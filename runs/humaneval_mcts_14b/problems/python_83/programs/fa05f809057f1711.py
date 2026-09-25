def starts_one_ends(n):
    if n == 1:
        return 1  # Only the number 1 itself

    # Numbers starting with 1: 1xxxx... (n-1 digits can be anything from 0 to 9)
    start_with_1 = 10**(n-1)

    # Numbers ending with 1: xxxx...1 (n-1 digits can be anything from 0 to 9)
    end_with_1 = 10**(n-1)

    # Numbers both starting and ending with 1: 1xxx...1 (n-2 digits can be anything from 0 to 9)
    start_and_end_with_1 = 10**(n-2)

    # Total count is the sum of numbers starting with 1 and ending with 1,
    # minus those counted twice (both starting and ending with 1)
    total_count = start_with_1 + end_with_1 - start_and_end_with_1

    return total_count