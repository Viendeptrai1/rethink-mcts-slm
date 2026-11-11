MOD = 1_000_000_007

def count_ways(N, M, broken_steps):
    dp = [0] * (N + 1)
    dp[0] = 1
    
    for i in range(1, N + 1):
        if i not in broken_steps:
            if i - 1 >= 0:
                dp[i] += dp[i - 1]
            if i - 2 >= 0:
                dp[i] += dp[i - 2]
            dp[i] %= MOD
    
    return dp[N]

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
M = int(data[1])
broken_steps = set(map(int, data[2:2+M]))

# Output the result
print(count_ways(N, M, broken_steps))