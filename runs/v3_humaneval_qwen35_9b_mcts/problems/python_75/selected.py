def is_multiply_prime(a):
    def get_prime_factors(n):
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors

    if a < 8:
        return False

    factors = get_prime_factors(a)
    return len(factors) == 3