def is_equal_to_sum_even(n):
    # The smallest sum of 4 positive even numbers is 2 + 2 + 2 + 2 = 8
    # Any number less than 8 cannot be expressed as the sum of 4 positive even numbers
    if n < 8:
        return False
    # If n is even and greater than or equal to 8, it can always be expressed as the sum of 4 positive even numbers
    return n % 2 == 0