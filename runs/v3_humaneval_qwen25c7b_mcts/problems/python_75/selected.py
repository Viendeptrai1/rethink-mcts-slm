from itertools import combinations

def is_multiply_prime(a):
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    primes = [i for i in range(2, 101) if is_prime(i)]
    
    for combo in combinations(primes, 3):
        if combo[0] * combo[1] * combo[2] == a:
            return True
    return False