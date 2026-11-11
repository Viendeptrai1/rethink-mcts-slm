import sys
from collections import defaultdict

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
    from itertools import combinations
    
    max_rev = 0
    for r in range(1, N + 1):
        for combo in combinations(range(N), r):
            total_sum = sum(S[i] for i in combo)
            prime_factors_count = count_distinct_prime_factors(total_sum)
            remaining_sum = sum(S[i] for i in range(N) if i not in combo)
            remaining_prime_factors_count = count_distinct_prime_factors(remaining_sum)
            max_rev = max(max_rev, prime_factors_count + remaining_prime_factors_count)
    
    return max_rev

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    S = list(map(int, data[1:]))
    
    print(max_revenue(N, S))

if __name__ == "__main__":
    main()