def is_equal_to_sum_even(n):
    """Evaluate whether the given number n can be written as the sum of exactly 4 positive even numbers"""
    # The smallest sum of 4 positive even numbers is 2 + 2 + 2 + 2 = 8
    # Any number less than 8 cannot be written as the sum of 4 positive even numbers
    if n < 8:
        return False
    # If n is even and greater than or equal to 8, it can always be written as the sum of 4 even numbers
    return n % 2 == 0