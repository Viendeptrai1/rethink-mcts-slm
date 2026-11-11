import sys
from itertools import combinations

def count_distinct_prime_factors(n):
    if n < 2:
        return 0
    count = 0
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            count += 1
            while n % factor == 0:
                n //= factor
        factor += 1
    if n > 1:
        count += 1
    return count

def max_revenue(N, S):
    max_revenue = 0
    for r in range(1, N + 1):
        for combo in combinations(S, r):
            total_sum = sum(combo)
            prime_factors_count = count_distinct_prime_factors(total_sum)
            max_revenue = max(max_revenue, prime_factors_count)
    return max_revenue

if __name__ == "__main__":
    N = int(sys.stdin.readline().strip())
    S = list(map(int, sys.stdin.readline().strip().split()))
    print(max_revenue(N, S))