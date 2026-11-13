def prime_fib(n: int) -> int:
    def is_prime(num: int) -> bool:
        if num < 2:
            return False
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True

    def fibonacci():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    found_primes = []
    for fib_number in fibonacci():
        if is_prime(fib_number):
            found_primes.append(fib_number)
            if len(found_primes) == n:
                return fib_number