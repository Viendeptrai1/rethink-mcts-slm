def is_prime(num: int) -> bool:
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    i = 3
    while i * i <= num:
        if num % i == 0:
            return False
        i += 2
    return True

def prime_fib(n: int) -> int:
    if n <= 0:
        raise ValueError("n must be a positive integer")
    
    count = 0
    a, b = 0, 1
    
    while True:
        if is_prime(a):
            count += 1
            if count == n:
                return a
        a, b = b, a + b