def bachgold_problem(n):
    # Function to check if a number is prime
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

    # List to store the prime numbers
    primes = []

    # Start with the largest possible prime less than or equal to n
    while n > 0:
        # Find the largest prime less than or equal to n
        for i in range(n, 1, -1):
            if is_prime(i):
                primes.append(i)
                n -= i
                break

    # Output the result
    print(len(primes))
    print(' '.join(map(str, primes)))

# Read input
n = int(input().strip())
bachgold_problem(n)