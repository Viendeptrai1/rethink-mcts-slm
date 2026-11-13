MOD = 10**9 + 7

def count_plaque_arrangements(n, k):
    if n == 1:
        return 1
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = (dp[i - 1] * (i - 1) + dp[i - 2]) % MOD
    
    if k == 1:
        return dp[n]
    
    total_ways = dp[n]
    invalid_ways = dp[k]
    
    result = (total_ways - invalid_ways + MOD) % MOD
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])

# Output result
print(count_plaque_arrangements(n, k))