def largest_prime_factor(n: int) -> int:
    def is_prime(x):
        if x < 2:
            return False
        for i in range(2, int(x ** 0.5) + 1):
            if x % i == 0:
                return False
        return True

    largest_factor = None
    # Check for smallest factors first
    for i in range(2, int(n ** 0.5) + 1):
        while n % i == 0:
            largest_factor = i
            n //= i
    # If there's anything left of n, it must be a prime number
    if n > 1:
        largest_factor = n

    return largest_factor