def skjkasdkd(lst):
    def is_prime(n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        return True

    def sum_of_digits(n):
        return sum(int(d) for d in str(n))

    primes = [x for x in lst if is_prime(x)]
    
    if not primes:
        return 0
    
    largest_prime = max(primes)
    return sum_of_digits(largest_prime)