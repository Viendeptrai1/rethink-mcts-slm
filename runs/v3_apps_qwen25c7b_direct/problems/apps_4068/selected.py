MOD = 1000000007

def count_ways(N, M, broken_steps):
    dp = [0] * (N + 1)
    dp[0] = 1
    
    for i in range(1, N + 1):
        if i not in broken_steps:
            dp[i] = (dp[i - 1] + dp[i - 2]) % MOD
    
    return dp[N]

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
M = int(data[1])
broken_steps = set(int(data[i]) for i in range(2, 2 + M))

# Calculate and print result
result = count_ways(N, M, broken_steps)
print(result)