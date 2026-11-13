from math import sqrt

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def is_multiply_prime(a):
    if a >= 100:
        return False
    primes = [i for i in range(2, 100) if is_prime(i)]
    count = 0
    for prime in primes:
        while a % prime == 0:
            a //= prime
            count += 1
        if count > 3:
            return False
    return count == 3 and a == 1