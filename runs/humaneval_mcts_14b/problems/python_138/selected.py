def is_equal_to_sum_even(n):
    """Evaluate whether the given number n can be written as the sum of exactly 4 positive even numbers"""
    if n < 8:
        return False
    # Check if n is even
    if n % 2 != 0:
        return False
    # Subtract the smallest sum of 4 even numbers (8) from n
    remaining = n - 8
    # Check if the remaining is even and non-negative
    return remaining % 2 == 0 and remaining >= 0