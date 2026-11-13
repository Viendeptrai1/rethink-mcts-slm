from math import sqrt

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def fib_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def prime_fib(n: int) -> int:
    count = 0
    for fib_num in fib_generator():
        if fib_num > 1 and is_prime(fib_num):
            count += 1
            if count == n:
                return fib_num