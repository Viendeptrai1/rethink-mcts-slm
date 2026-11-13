MOD = 998244853

def max_prefix_sum(n, m):
    if n == 0:
        return 0
    if m == 0:
        return n
    
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        dp[i][0] = i
    
    for j in range(1, m + 1):
        dp[0][j] = -j
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    result = 0
    for i in range(n + 1):
        for j in range(m + 1):
            result += dp[i][j]
            result %= MOD
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])

# Output result
print(max_prefix_sum(n, m))