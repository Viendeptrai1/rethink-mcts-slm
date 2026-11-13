def starts_one_ends(n):
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
    if n == 1:
        # 1-digit numbers: only '1' starts and ends with 1
        return 1
    
    # Total n-digit numbers
    total = 9 * (10 ** (n - 1))
    
    # Numbers starting with 1: 1 followed by any n-1 digits
    starts_with_1 = 10 ** (n - 1)
    
    # Numbers ending with 1: first digit can be 1-9, last is 1, middle n-2 digits any
    ends_with_1 = 9 * (10 ** (n - 2))
    
    # Numbers both starting and ending with 1: 1...1
    both = 10 ** (n - 2)
    
    # Use inclusion-exclusion principle
    return starts_with_1 + ends_with_1 - both