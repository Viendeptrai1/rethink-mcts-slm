from math import sqrt

def is_prime(num: int) -> bool:
    if num <= 1:
        return False
    for i in range(2, int(sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def prime_fib(n: int) -> int:
    def fib_generator():
        a, b = 0, 1
        while True:
            yield b
            a, b = b, a + b
    
    count = 0
    for fib_num in fib_generator():
        if is_prime(fib_num):
            count += 1
            if count == n:
                return fib_num