MOD = 10**9 + 7

def count_random_pictures(n, m):
    if n == 1:
        return pow(2, m, MOD)
    if m == 1:
        return pow(2, n, MOD)
    
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    dp[1][1] = 2
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if i == 1 and j == 1:
                continue
            dp[i][j] = (dp[i-1][j] + dp[i][j-1]) % MOD
    
    return dp[n][m]

# Input reading
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])

# Output result
print(count_random_pictures(n, m))