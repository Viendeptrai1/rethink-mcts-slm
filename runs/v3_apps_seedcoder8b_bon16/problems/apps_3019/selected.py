import sys
from itertools import combinations
from math import gcd

def prime_factors(n):
    factors = set()
    d = 2
    while n > 1:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
        if d * d > n:
            if n > 1:
                factors.add(n)
            break
    return factors

def max_revenue(N, S):
    def revenue(group):
        return len(prime_factors(sum(S[i-1] for i in group)))

    max_rev = 0
    for r in range(1, N+1):
        for group in combinations(range(1, N+1), r):
            rev = revenue(group)
            remaining = tuple(i for i in range(1, N+1) if i not in group)
            if not remaining:
                max_rev = max(max_rev, rev)
            else:
                max_rev = max(max_rev, rev + max_revenue(len(remaining), [S[i-1] for i in remaining]))

    return max_rev

def main():
    N = int(input())
    S = list(map(int, input().split()))
    print(max_revenue(N, S))

if __name__ == "__main__":
    main()