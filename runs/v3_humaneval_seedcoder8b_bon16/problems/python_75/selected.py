def is_multiply_prime(a):
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True
    
    prime_count = 0
    for i in range(2, a + 1):
        if is_prime(i) and a % i == 0:
            a //= i
            prime_count += 1
        if prime_count > 3:
            return False
    return prime_count == 3