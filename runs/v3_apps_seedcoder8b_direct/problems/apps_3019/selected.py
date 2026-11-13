import sys
from itertools import combinations
from math import isqrt

def prime_factors_count(n):
    count = 0
    if n <= 1:
        return count
    for i in range(2, isqrt(n) + 1):
        if n % i == 0:
            count += 1
            while n % i == 0:
                n //= i
    if n > 1:
        count += 1
    return count

def max_revenue(N, S):
    max_rev = 0
    for r in range(1, N + 1):
        for combo in combinations(range(N), r):
            sum_s = sum(S[i] for i in combo)
            rev = prime_factors_count(sum_s)
            max_rev = max(max_rev, rev)
    return max_rev

def main():
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    S = list(map(int, data[1:N+1]))
    print(max_revenue(N, S))

if __name__ == "__main__":
    main()