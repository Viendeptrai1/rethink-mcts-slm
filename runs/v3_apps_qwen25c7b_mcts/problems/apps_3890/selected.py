MOD = 10**9 + 7

def count_ways(n, k):
    if k == 1:
        return pow(n, n-1, MOD)
    
    dp = [[0] * (n+1) for _ in range(n+1)]
    dp[1][1] = 1
    
    for i in range(1, n+1):
        for j in range(1, n+1):
            if j <= k:
                dp[i][j] = (dp[i][j] + dp[i-1][j]) % MOD
            else:
                dp[i][j] = (dp[i][j] + dp[i-1][j] + dp[i-1][1]) % MOD
    
    result = 0
    for j in range(1, n+1):
        result = (result + dp[n][j]) % MOD
    
    return result

# Input reading
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

# Output the result
print(count_ways(n, k))