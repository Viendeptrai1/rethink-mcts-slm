def largest_prime_factor(n: int) -> int:
    # Start with the smallest prime number
    factor = 2
    
    # Divide n by factor until it is no longer divisible
    while n % factor == 0:
        n //= factor
    
    # Check for odd factors from 3 onwards
    factor = 3
    while factor * factor <= n:
        while n % factor == 0:
            n //= factor
        factor += 2
    
    # If n is still greater than 2, then it is prime
    if n > 2:
        return n
    
    return factor

# Test cases
print(largest_prime_factor(13195))  # Output: 29
print(largest_prime_factor(2048))   # Output: 2