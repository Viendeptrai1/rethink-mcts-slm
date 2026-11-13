from typing import List
import sys

def max_revenue(N: int, S: List[int]) -> int:
    def count_prime_factors(n):
        count = 0
        while n % 2 == 0:
            count += 1
            n //= 2
        for i in range(3, int(n**0.5) + 1, 2):
            while n % i == 0:
                count += 1
                n //= i
        if n > 2:
            count += 1
        return count

    dp = [0] * (1 << N)
    for mask in range(1, 1 << N):
        subset_sum = sum(S[i] for i in range(N) if mask & (1 << i))
        dp[mask] = count_prime_factors(subset_sum)

    return max(dp)

# Read input
input = sys.stdin.read
data = input().split()
N = int(data[0])
S = list(map(int, data[1:]))

# Output result
print(max_revenue(N, S))