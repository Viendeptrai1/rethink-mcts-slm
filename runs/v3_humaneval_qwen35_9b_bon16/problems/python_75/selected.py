def is_multiply_prime(a):
    if a < 2:
        return False
    
    def is_prime(n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    prime_factors = []
    temp = a
    d = 2
    while d * d <= temp:
        while temp % d == 0:
            prime_factors.append(d)
            temp //= d
        d += 1
    if temp > 1:
        prime_factors.append(temp)
    
    return len(prime_factors) == 3