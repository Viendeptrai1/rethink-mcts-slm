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
    max_rev = 0
    for i in range(1, 1 << N):
        total_sum = 0
        for j in range(N):
            if i & (1 << j):
                total_sum += S[j]
        max_rev = max(max_rev, count_distinct_prime_factors(total_sum))
    return max_rev

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    S = list(map(int, data[1:]))
    
    print(max_revenue(N, S))