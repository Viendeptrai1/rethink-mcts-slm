import math

def largest_prime_factor(n: int) -> int:
    """Return the largest prime factor of n. Assume n > 1 and is not a prime."""
    # Start with the smallest prime factor
    factor = 2
    
    # Iterate over potential factors from 2 up to the square root of n
    while factor <= math.sqrt(n):
        # If factor divides n, divide n by this factor as many times as possible
        while n % factor == 0:
            n //= factor
        # Move to the next potential factor
        factor += 1
    
    # When n is reduced to 1, the last factor used is the largest prime factor
    return factor - 1

# Test cases
print(largest_prime_factor(13195))  # Output: 29
print(largest_prime_factor(2048))   # Output: 2