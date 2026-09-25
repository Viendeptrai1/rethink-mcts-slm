def prime_length(string):
    def is_prime(n):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    return is_prime(len(string))

# Test cases
print(prime_length('Hello'))    # True
print(prime_length('abcdcba'))  # True
print(prime_length('kittens'))  # True
print(prime_length('orange'))   # False