def largest_prime_factor(n: int) -> int:
    def is_prime(num):
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

    largest_factor = None
    # Check for number of 2s that divide n
    while n % 2 == 0:
        largest_factor = 2
        n //= 2

    # n must be odd at this point, so a skip of 2 (i.e., i = i + 2) can be used
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            largest_factor = i
            n //= i

    # This condition is to check if n is a prime number greater than 2
    if n > 2:
        largest_factor = n

    return largest_factor