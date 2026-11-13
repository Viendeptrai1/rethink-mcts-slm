import sys
from itertools import combinations
from math import isqrt

def prime_factors_count(n):
    count = 0
    if n % 2 == 0:
        count += 1
        while n % 2 == 0:
            n //= 2
    for i in range(3, isqrt(n) + 1, 2):
        if n % i == 0:
            count += 1
            while n % i == 0:
                n //= i
    if n > 2:
        count += 1
    return count

def max_revenue(N, S):
    max_rev = 0
    for r in range(1, N + 1):
        for combo in combinations(range(N), r):
            sums = [sum(S[i] for i in combo)]
            for i in range(N):
                if i not in combo:
                    sums.append(S[i])
            revenue = sum(prime_factors_count(s) for s in sums)
            max_rev = max(max_rev, revenue)
    return max_rev

def main():
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    S = list(map(int, data[1:]))
    print(max_revenue(N, S))

if __name__ == "__main__":
    main()