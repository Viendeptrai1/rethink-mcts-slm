def largest_prime_factor(n: int) -> int:
    def is_prime(num):
        if num <= 1:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(num**0.5) + 1, 2):
            if num % i == 0:
                return False
        return True

    largest_factor = None
    for i in range(2, n + 1):
        while n % i == 0 and is_prime(i):
            largest_factor = i
            n //= i
    return largest_factor