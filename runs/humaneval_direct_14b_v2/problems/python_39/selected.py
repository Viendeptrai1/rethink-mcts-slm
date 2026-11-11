from math import sqrt

def is_prime(num: int) -> bool:
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def prime_fib(n: int) -> int:
    if n <= 0:
        raise ValueError("n must be a positive integer")
    
    fib1, fib2 = 0, 1
    count = 0
    
    while True:
        fib_next = fib1 + fib2
        fib1, fib2 = fib2, fib_next
        
        if is_prime(fib_next):
            count += 1
            if count == n:
                return fib_next