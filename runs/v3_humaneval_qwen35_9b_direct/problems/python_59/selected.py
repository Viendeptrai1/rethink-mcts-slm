def largest_prime_factor(n: int) -> int:
    """Return the largest prime factor of n. Assume n > 1 and is not a prime.
    >>> largest_prime_factor(13195)
    29
    >>> largest_prime_factor(2048)
    2
    """
    factor = 2
    max_factor = 2
    
    # Handle factor 2 separately to allow skipping even numbers later
    while n % factor == 0:
        max_factor = factor
        n //= factor
    
    # Check for odd factors from 3 upwards
    factor = 3
    while factor * factor <= n:
        while n % factor == 0:
            max_factor = factor
            n //= factor
        factor += 2
    
    # If n is now greater than 1, then the remaining n is a prime factor
    if n > 1:
        max_factor = n
    
    return max_factor