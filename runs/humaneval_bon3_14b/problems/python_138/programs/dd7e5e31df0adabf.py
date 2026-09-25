def is_equal_to_sum_even(n):
    """Evaluate whether the given number n can be written as the sum of exactly 4 positive even numbers"""
    # The smallest sum of 4 positive even numbers is 2 + 2 + 2 + 2 = 8
    # Any number less than 8 cannot be written as the sum of 4 positive even numbers
    if n < 8:
        return False
    
    # For any number n >= 8, it can be written as the sum of 4 positive even numbers
    # For example, n = 8 can be written as 2 + 2 + 2 + 2
    # For n > 8, we can always adjust the numbers to make their sum equal to n
    # For instance, if n is even, we can use (n-8) + 2 + 2 + 2
    # If n is odd, we can use (n-9) + 2 + 2 + 3
    return True