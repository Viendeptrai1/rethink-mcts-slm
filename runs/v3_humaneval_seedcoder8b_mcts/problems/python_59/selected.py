def largest_prime_factor(n: int) -> int:
    def is_prime(x: int) -> bool:
        if x <= 1:
            return False
        if x <= 3:
            return True
        if x % 2 == 0 or x % 3 == 0:
            return False
        i = 5
        while i * i <= x:
            if x % i == 0 or x % (i + 2) == 0:
                return False
            i += 6
        return True

    largest_factor = 1
    # Check for smallest prime factor 2
    while n % 2 == 0:
        largest_factor = 2
        n //= 2

    # Check for odd factors from 3 onwards
    factor = 3
    while factor * factor <= n:
        while n % factor == 0:
            largest_factor = factor
            n //= factor
        factor += 2

    # If n is still greater than 2, then n itself is a prime number
    if n > 2:
        largest_factor = n

    return largest_factor