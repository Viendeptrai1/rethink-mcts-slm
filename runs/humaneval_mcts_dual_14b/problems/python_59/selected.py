def largest_prime_factor(n: int) -> int:
    # Step 1: Remove all factors of 2
    while n % 2 == 0:
        largest_factor = 2
        n //= 2
    
    # Step 2: Check for odd factors from 3 onwards
    factor = 3
    while factor * factor <= n:
        while n % factor == 0:
            largest_factor = factor
            n //= factor
        factor += 2
    
    # If n is still greater than 2, then it is prime
    if n > 2:
        largest_factor = n
    
    return largest_factor