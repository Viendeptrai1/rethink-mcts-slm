def starts_one_ends(n):
    if n == 1:
        return 1  # Only the number 1 itself

    # Numbers that start with 1
    start_with_1 = 10**(n-1)
    
    # Numbers that end with 1
    end_with_1 = 9 * 10**(n-2)
    
    # Numbers that both start and end with 1
    both_start_and_end_with_1 = 10**(n-2)
    
    # Total numbers that start or end with 1
    total = start_with_1 + end_with_1 - both_start_and_end_with_1
    
    return total