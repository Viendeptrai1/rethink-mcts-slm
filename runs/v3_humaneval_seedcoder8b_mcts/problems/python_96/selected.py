def count_up_to(n):
    if n <= 2:
        return []
    
    # Initialize a list to track prime status of numbers
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False  # 0 and 1 are not prime numbers
    
    # Implement the Sieve of Eratosthenes
    for start in range(2, int(n**0.5) + 1):
        if is_prime[start]:
            for multiple in range(start*start, n, start):
                is_prime[multiple] = False
    
    # Collect all prime numbers less than n
    primes = [num for num, prime in enumerate(is_prime) if prime]
    
    return primes