def largest_prime_factor(n: int) -> int:
    """Return the largest prime factor of n. Assume n > 1 and is not a prime."""
    factor = 2
    while n > 1:
        if n % factor == 0:
            n //= factor
        else:
            factor += 1
    return factor

# Test cases
print(largest_prime_factor(13195))  # Output: 29
print(largest_prime_factor(2048))   # Output: 2