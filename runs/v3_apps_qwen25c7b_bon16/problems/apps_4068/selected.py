def count_ways(N, M, broken_steps):
    MOD = 1000000007
    dp = [0] * (N + 1)
    dp[0] = 1
    
    broken_set = set(broken_steps)
    
    for i in range(1, N + 1):
        if i not in broken_set:
            dp[i] = (dp[i - 1] + dp[i - 2]) % MOD
    
    return dp[N]

# Input reading
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
M = int(data[1])
broken_steps = list(map(int, data[2:]))

# Calculate and print the result
result = count_ways(N, M, broken_steps)
print(result)