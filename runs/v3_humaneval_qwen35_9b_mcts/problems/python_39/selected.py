import math

def is_prime(num: int) -> bool:
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    limit = int(math.isqrt(num)) + 1
    for i in range(3, limit, 2):
        if num % i == 0:
            return False
    return True

def prime_fib(n: int) -> int:
    if n <= 0:
        raise ValueError("n must be a positive integer")
    
    count = 0
    a, b = 0, 1
    
    while True:
        if is_prime(b):
            count += 1
            if count == n:
                return b
        a, b = b, a + b