from sympy import isprime

def prime_fib(n: int) -> int:
    def fib_generator():
        a, b = 0, 1
        while True:
            yield b
            a, b = b, a + b

    count = 0
    for fib_num in fib_generator():
        if fib_num > 1 and isprime(fib_num):
            count += 1
            if count == n:
                return fib_num