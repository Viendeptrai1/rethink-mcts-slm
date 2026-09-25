def starts_one_ends(n):
    if n == 1:
        return 1
    
    # Calculate numbers starting with 1
    start_with_1 = 10 ** (n - 1)
    
    # Calculate numbers ending with 1
    end_with_1 = 9 * (10 ** (n - 2))
    
    # Subtract the overlap where numbers both start and end with 1
    overlap = 10 ** (n - 2)
    
    return start_with_1 + end_with_1 - overlap