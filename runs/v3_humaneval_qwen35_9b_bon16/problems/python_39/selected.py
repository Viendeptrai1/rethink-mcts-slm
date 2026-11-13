def prime_fib(n: int) -> int:
    if n <= 0:
        raise ValueError("n must be a positive integer")
    
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

    a, b = 0, 1
    count = 0
    while count < n:
        if is_prime(b):
            count += 1
            if count == n:
                return b
        a, b = b, a + b

    return b