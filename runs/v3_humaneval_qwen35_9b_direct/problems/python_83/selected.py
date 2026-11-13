def starts_one_ends(n):
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
    if n == 1:
        return 1
    
    # Total n-digit numbers: 9 * 10^(n-1)
    # Start with 1: 1 * 10^(n-1)
    # End with 1: 9 * 10^(n-2)
    # Both start and end with 1: 1 * 10^(n-2)
    
    start_with_1 = 10**(n-1)
    end_with_1 = 9 * 10**(n-2)
    both = 10**(n-2)
    
    return start_with_1 + end_with_1 - both