import math

def largest_prime_factor(n: int) -> int:
    # Initialize the smallest prime factor
    factor = 2
    
    while factor * factor <= n:
        if n % factor == 0:
            n //= factor
        else:
            factor += 1
    
    return n