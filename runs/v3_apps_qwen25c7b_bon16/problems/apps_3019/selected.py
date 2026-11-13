from sys import stdin

def count_distinct_prime_factors(n):
    factors = set()
    # Check divisibility by 2
    while n % 2 == 0:
        factors.add(2)
        n //= 2
    # Check for odd factors
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            factors.add(i)
            n //= i
    # If n is a prime number greater than 2
    if n > 2:
        factors.add(n)
    return len(factors)

def max_revenue(N, S):
    total_sum = sum(S)
    return count_distinct_prime_factors(total_sum)

# Read input
N = int(stdin.readline())
S = list(map(int, stdin.readline().split()))

# Calculate and print the maximum revenue
print(max_revenue(N, S))