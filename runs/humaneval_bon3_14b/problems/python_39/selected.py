from sympy import isprime

def prime_fib(n: int) -> int:
    def fibonacci():
        a, b = 0, 1
        while True:
            yield b
            a, b = b, a + b

    count = 0
    for fib_num in fibonacci():
        if isprime(fib_num):
            count += 1
            if count == n:
                return fib_num

# Example usage:
# print(prime_fib(1))  # Output: 2
# print(prime_fib(2))  # Output: 3
# print(prime_fib(3))  # Output: 5
# print(prime_fib(4))  # Output: 13
# print(prime_fib(5))  # Output: 89