from sympy import isprime

def prime_fib(n: int) -> int:
    def fibonacci():
        a, b = 0, 1
        while True:
            yield b
            a, b = b, a + b

    count = 0
    for fib_number in fibonacci():
        if isprime(fib_number):
            count += 1
            if count == n:
                return fib_number