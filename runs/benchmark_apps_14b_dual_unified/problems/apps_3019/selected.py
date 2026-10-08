import sys
from math import sqrt

def count_distinct_prime_factors(n):
    if n < 2:
        return 0
    count = 0
    if n % 2 == 0:
        count += 1
        while n % 2 == 0:
            n //= 2
    for i in range(3, int(sqrt(n)) + 1, 2):
        if n % i == 0:
            count += 1
            while n % i == 0:
                n //= i
    if n > 2:
        count += 1
    return count

def max_revenue(N, S):
    dp = [0] * (1 << N)
    for mask in range(1, 1 << N):
        total_sum = 0
        for j in range(N):
            if mask & (1 << j):
                total_sum += S[j]
        dp[mask] = count_distinct_prime_factors(total_sum)
        for submask in range(mask):
            if (mask & submask) == submask:
                dp[mask] = max(dp[mask], dp[submask] + dp[mask ^ submask])
    return dp[(1 << N) - 1]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    S = list(map(int, data[1:]))
    
    print(max_revenue(N, S))

if __name__ == "__main__":
    main()