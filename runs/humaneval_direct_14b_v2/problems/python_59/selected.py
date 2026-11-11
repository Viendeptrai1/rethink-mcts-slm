def largest_prime_factor(n: int) -> int:
    # Initialize the smallest prime factor
    factor = 2
    
    # Divide n by 2 until it becomes odd
    while n % factor == 0:
        n //= factor
    
    # Check for odd factors from 3 onwards
    factor = 3
    while factor * factor <= n:
        while n % factor == 0:
            n //= factor
        factor += 2
    
    # If n is still greater than 2, then it is prime
    return n if n > 2 else factor