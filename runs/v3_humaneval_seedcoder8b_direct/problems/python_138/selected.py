def is_equal_to_sum_even(n):
    if n < 8:
        return False
    
    for a in range(2, n-5, 2):
        for b in range(a+2, n-3, 2):
            for c in range(b+2, n-1, 2):
                d = n - a - b - c
                if d > c and d % 2 == 0:
                    return True
    
    return False