def largest_prime_factor(n: int) -> int:
    """Return the largest prime factor of n. Assume n > 1 and is not a prime.
    >>> largest_prime_factor(13195)
    29
    >>> largest_prime_factor(2048)
    2
    """
    factor = 2
    largest = -1

    # Divide by 2 until it's no longer divisible
    while n % factor == 0:
        largest = factor
        n //= factor

    # Check odd factors from 3 upwards
    factor = 3
    while factor * factor <= n:
        while n % factor == 0:
            largest = factor
            n //= factor
        factor += 2

    # If n is now greater than 1, then the remaining n is a prime
    if n > 1:
        largest = n

    return largest